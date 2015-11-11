from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.forms import (Form, HiddenInput, IntegerField, ModelForm,
                          ModelChoiceField, ModelMultipleChoiceField,
                          ValidationError)
from django.utils.safestring import mark_safe

from ajax_select.fields import AutoCompleteSelectField
from floppyforms.widgets import SelectMultiple

from accounts.utils import get_profile
from .models import Garden, GardenGroup, GardenGroupMembership, GardenType


class AddNewGardenGroupWidget(SelectMultiple):
    template_name = 'farmingconcrete/gardengroup/new_gardengroup_widget.html'


class GardenTypeField(ModelChoiceField):
    """
    A ModelChoiceField for GardenTypes that restricts a user's options based
    on its profile.
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not 'queryset' in kwargs:
            kwargs['queryset'] = GardenType.objects.all()
        super(GardenTypeField, self).__init__(*args, **kwargs)

        if user and not user.has_perm('can_edit_any_garden'):
            profile = get_profile(user)
            if profile.garden_types.count() > 0:
                self.queryset = self.queryset & profile.garden_types.all()


class FindGardenForm(Form):
    type = GardenTypeField()
    garden = AutoCompleteSelectField('garden', required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FindGardenForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['type'] = GardenTypeField(
                queryset=self.fields['type'].queryset,
                user=user
            )


class GardenForm(ModelForm):
    id = IntegerField(
        required=False,
        widget=HiddenInput(),
    )
    type = GardenTypeField()
    groups = ModelMultipleChoiceField(
        queryset=GardenGroup.objects.all().order_by('name'),
        required=False,
        widget=AddNewGardenGroupWidget(),
    )
    edited_by = ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=HiddenInput(),
    )

    def _privacy_fields(self):
        return [self[name] for name in ('share_name', 'share_location',)]
    privacy_fields = property(_privacy_fields)

    class Meta:
        model = Garden
        exclude = ('gardenid', 'added', 'updated', 'has_metric_records',
                   'metric_record_added', 'metric_records_count',)
        widgets = {
            'added_by': HiddenInput(),
            'latitude': HiddenInput(),
            'longitude': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GardenForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['type'] = GardenTypeField(
                queryset=self.fields['type'].queryset,
                user=self.user
            )

    def clean_groups(self):
        """
        Ensure that all groups:
         * are open OR
         * already have the garden in them OR
         * have the adding user as an admin
        """
        groups = self.cleaned_data['groups']
        garden = None

        try:
            garden = Garden.objects.get(pk=self.cleaned_data['id'])
        except Garden.DoesNotExist:
            # Must be adding a new garden
            pass
        failures = filter(
            lambda g: not g.can_join(garden=garden, user=self.user),
            groups
        )
        if failures:
            errors = []
            for failure in failures:
                if garden:
                    url = reverse('farmingconcrete_gardengroup_request', kwargs={
                        'pk': failure.pk,
                    }) + '?garden=%s&user=%s' % (garden.pk or '', self.user.pk)
                    errors.append("""
<p class="group-permission-required-message">
    %s is not an open group. 
    <a href="%s" class="request-group-permission">Ask for permission</a> to join it.
</p>""" % (failure.name, url))
                else:
                    errors.append("""
<p class="group-permission-required-message">
    %s is not an open group. Please remove it from this list, save this garden,
    and then try adding the garden to it. You will then be able to request 
    permission to join it.
</p>""" % failure.name)
            raise ValidationError(mark_safe(''.join(errors)))
        return groups

    def clean(self):
        cleaned_data = super(GardenForm, self).clean()

        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if not latitude or not longitude:
            raise ValidationError("""
                A point was not found for the address you entered. Please
                enter the address again and ensure that the correct point is
                shown on the map for the garden you're adding.
            """)

        # If we're editing the garden and it has a latitude and longitude,
        # that's good enough
        if cleaned_data.get('id'):
            return cleaned_data

        # Disallow gardens at the same address, city, and state as an existing
        # one.
        address_kwargs = {
            'address': cleaned_data.get('address'),
            'city': cleaned_data.get('city'),
            'state': cleaned_data.get('state'),
        }
        if Garden.objects.filter(**address_kwargs).exists():
            raise ValidationError("""
                The address you entered is too similar to an existing garden's
                address. Please change the address or pick the garden from the
                list on the right. Contact us if you think this is a mistake.
            """)

        # Disallow gardens at the same latitude and longitude as an existing
        # one.
        centroid_kwargs = {
            'latitude': latitude,
            'longitude': longitude,
        }
        if Garden.objects.filter(**centroid_kwargs).exists():
            raise ValidationError("""
                The location you entered is too similar to an existing garden's
                address. Please change the address or pick the garden from the
                list on the right. Contact us if you think this is a mistake.
            """)

        return cleaned_data

    def save(self, *args, **kwargs):
        user = self.cleaned_data['edited_by']
        groups = self.cleaned_data['groups']
        garden = super(GardenForm, self).save(*args, **kwargs)
        GardenGroupMembership.objects.filter(garden=garden).delete()
        for group in groups:
            membership = GardenGroupMembership(
                added_by=user,
                garden=garden,
                group=group,
            )
            membership.save()
        return garden


class GardenGroupForm(ModelForm):

    class Meta:
        model = GardenGroup
        exclude = ('description', 'gardens',)
        widgets = {
            'added_by': HiddenInput(),
            'needs_moderation': HiddenInput(),
            'updated_by': HiddenInput(),
        }


class InviteGardenForm(Form):
    garden = AutoCompleteSelectField('garden', required=True)

    def __init__(self, group=None, *args, **kwargs):
        super(InviteGardenForm, self).__init__(*args, **kwargs)
        self.group = group

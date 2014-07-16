from django.contrib.auth import get_user_model
from django.forms import (Form, HiddenInput, ModelForm, ModelChoiceField,
                          ValidationError)

from ajax_select.fields import AutoCompleteSelectField
import chosen.forms

from accounts.utils import get_profile
from .models import Garden, GardenGroup, GardenGroupMembership, GardenType


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
    type = GardenTypeField()
    groups = chosen.forms.ChosenModelMultipleChoiceField(
        queryset=GardenGroup.objects.all().order_by('name'),
        required=False,
    )
    added_by = ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=HiddenInput(),
    )

    class Meta:
        model = Garden
        exclude = ('gardenid', 'added', 'updated')
        widgets = {
            'latitude': HiddenInput(),
            'longitude': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GardenForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['type'] = GardenTypeField(
                queryset=self.fields['type'].queryset,
                user=user
            )

    def clean(self):
        cleaned_data = super(GardenForm, self).clean()

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
            'latitude': cleaned_data.get('latitude'),
            'longitude': cleaned_data.get('longitude'),
        }
        if Garden.objects.filter(**centroid_kwargs).exists():
            raise ValidationError("""
                The location you entered is too similar to an existing garden's
                address. Please change the address or pick the garden from the
                list on the right. Contact us if you think this is a mistake.
            """)

        return cleaned_data

    def save(self, *args, **kwargs):
        user = self.cleaned_data['added_by']
        groups = self.cleaned_data['groups']
        garden = super(GardenForm, self).save(*args, **kwargs)
        garden.gardengroup_set.clear()
        for group in groups:
            membership = GardenGroupMembership(
                added_by=user,
                garden=garden,
                group=group,
            )
            membership.save()
        return garden

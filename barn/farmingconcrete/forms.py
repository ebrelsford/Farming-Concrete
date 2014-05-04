from django.contrib.auth.models import User
from django.forms import (Form, HiddenInput, ModelForm, ModelChoiceField)

from ajax_select.fields import AutoCompleteSelectField
import chosen.forms
from floppyforms.widgets import Select

from accounts.models import UserProfile
from accounts.utils import get_profile
from .models import (Garden, GardenGroup, GardenGroupMembership, GardenType,
                     Variety)


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
            try:
                profile = get_profile(user)
                if profile and profile.garden_types.count() > 0:
                    self.queryset = self.queryset & profile.garden_types.all()
            except UserProfile.DoesNotExist:
                pass


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
        queryset=User.objects.all(),
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


class AddNewVarietyWidget(Select):
    template_name = 'farmingconcrete/variety/new_variety_widget.html'


class VarietyForm(ModelForm):

    class Meta:
        model = Variety
        widgets = {
            'added_by': HiddenInput(),
            'needs_moderation': HiddenInput(),
            'updated_by': HiddenInput(),
        }

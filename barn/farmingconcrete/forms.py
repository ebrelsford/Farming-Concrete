from django.forms import Form, ModelForm, ModelChoiceField

from ajax_select.fields import AutoCompleteSelectField

from accounts.models import UserProfile
from farmingconcrete.models import Garden, GardenType

class GardenTypeField(ModelChoiceField):
    """A ModelChoiceField for GardenTypes that restricts a user's options based on its profile."""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not 'queryset' in kwargs:
            kwargs['queryset'] = GardenType.objects.all()
        super(GardenTypeField, self).__init__(*args, **kwargs)

        if user and not user.has_perm('can_edit_any_garden'):
            try:
                profile = user.get_profile()
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
            self.fields['type'] = GardenTypeField(queryset=self.fields['type'].queryset, user=user)

class GardenForm(ModelForm):
    type = GardenTypeField()

    class Meta:
        model = Garden
        exclude = ('gardenid', 'longitude', 'latitude', 'added', 'updated')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GardenForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['type'] = GardenTypeField(queryset=self.fields['type'].queryset, user=user)

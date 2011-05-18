from django.forms import Form, ModelChoiceField
from ajax_select.fields import AutoCompleteSelectField

from farmingconcrete.models import GardenType
from farmingconcrete.forms import GardenTypeField
from accounts.models import UserProfile

class UncountedGardenForm(Form):
    type = GardenTypeField()
    garden = AutoCompleteSelectField('uncounted_garden', required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UncountedGardenForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['type'] = GardenTypeField(queryset=self.fields['type'].queryset, user=user)

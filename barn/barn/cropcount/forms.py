from django.forms import Form, ChoiceField
from ajax_select.fields import AutoCompleteSelectField

from farmingconcrete.models import Garden

class UncountedGardenForm(Form):
    type = ChoiceField(choices=Garden.TYPE_CHOICES)
    garden = AutoCompleteSelectField('uncounted_garden', required=True)

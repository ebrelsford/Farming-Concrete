from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from floppyforms.widgets import TimeInput

from ..forms import RecordedField, RecordForm
from .models import LookingGoodEvent, LookingGoodTag


class LookingGoodTagForm(ModelForm):

    class Meta:
        model = LookingGoodTag


LookingGoodTagFormSet = inlineformset_factory(LookingGoodEvent, LookingGoodTag,
    can_delete=False,
    extra=1,
    form=LookingGoodTagForm,
)

class LookingGoodEventForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )

    class Meta:
        model = LookingGoodEvent
        fields = ('recorded', 'start_time', 'end_time', 'total_tags',
                  'added_by', 'garden',)
        widgets = {
            'end_time': TimeInput,
            'start_time': TimeInput,
        }

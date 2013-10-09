from floppyforms.widgets import TimeInput

from ..forms import RecordedField, RecordForm
from .models import LookingGoodEvent


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

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from floppyforms.widgets import TimeInput

from ..forms import RecordedField, RecordForm
from .models import LookingGoodEvent, LookingGoodPhoto


class LookingGoodPhotoForm(ModelForm):

    class Meta:
        model = LookingGoodPhoto


LookingGoodPhotoFormSet = inlineformset_factory(LookingGoodEvent, LookingGoodPhoto,
    can_delete=False,
    extra=1,
    form=LookingGoodPhotoForm,
)

class EventTimeInput(TimeInput):

    def __init__(self, attrs=None, *args, **kwargs):
        try:
            if not attrs or not 'step' in attrs:
                attrs = {}
                attrs['step'] = 5 * 60 # 5 minutes
        except Exception:
            pass
        super(EventTimeInput, self).__init__(attrs=attrs, *args, **kwargs)


class LookingGoodEventForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )

    class Meta:
        model = LookingGoodEvent
        fields = ('recorded', 'start_time', 'end_time', 'total_tags',
                  'comments', 'added_by', 'garden',)
        widgets = {
            'end_time': EventTimeInput,
            'start_time': EventTimeInput,
        }

from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm
from django.utils.timezone import now

from floppyforms.fields import DateField
from floppyforms.widgets import DateInput

from farmingconcrete.models import Garden


class RecordedInput(DateInput):
    template_name = 'metrics/forms/recorded_input.html'

    def __init__(self, attrs=None, *args, **kwargs):
        try:
            if not attrs or not 'max' in attrs:
                attrs = {}
            attrs['max'] = now().date().isoformat()
        except Exception:
            pass
        super(RecordedInput, self).__init__(attrs=attrs, *args, **kwargs)


class RecordedField(DateField):
    widget = RecordedInput


class RecordForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())

    recorded = RecordedField(label='Date recorded', required=True)

    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        fields = ('recorded', 'added_by', 'garden',)

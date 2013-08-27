from datetime import date

from django.contrib.auth.models import User
from django.forms import DateInput, HiddenInput, ModelChoiceField, ModelForm

from farmingconcrete.models import Garden


class RecordedInput(DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, *args, **kwargs):
        try:
            if not attrs or not 'max' in attrs:
                attrs = {}
            attrs['max'] = date.today().isoformat()
        except Exception:
            pass
        super(RecordedInput, self).__init__(attrs=attrs)


class RecordForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

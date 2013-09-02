from datetime import date

from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm

from floppyforms.fields import DateField
from floppyforms.widgets import DateInput

from farmingconcrete.models import Garden


class RecordedInput(DateInput):

    def __init__(self, attrs=None, *args, **kwargs):
        try:
            if not attrs or not 'max' in attrs:
                attrs = {}
            attrs['max'] = date.today().isoformat()
        except Exception:
            pass
        super(RecordedInput, self).__init__(attrs=attrs, *args, **kwargs)


class RecordedField(DateField):
    widget = RecordedInput


class RecordForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

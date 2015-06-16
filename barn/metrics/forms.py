from django.contrib.auth import get_user_model
from django.forms import HiddenInput, ModelChoiceField, ModelForm
from django.utils.timezone import now

from floppyforms.fields import DateField
from floppyforms.widgets import DateInput

from farmingconcrete.models import Garden


class RecordedInput(DateInput):
    template_name = 'metrics/forms/recorded_input.html'

    def render(self, name, value, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs['max'] = now().date().isoformat()
        return super(RecordedInput, self).render(name, value, attrs=attrs,
                                                 **kwargs)


class RecordedField(DateField):
    widget = RecordedInput


class RecordForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())

    recorded = RecordedField(label='Date recorded', required=True)

    added_by = ModelChoiceField(
        label='added_by',
        queryset=get_user_model().objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        fields = ('recorded', 'added_by', 'garden',)

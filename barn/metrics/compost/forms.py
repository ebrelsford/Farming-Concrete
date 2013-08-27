from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm

from farmingconcrete.models import Garden
from ..forms import RecordedInput
from .models import CompostProductionVolume, CompostProductionWeight


class CompostProductionWeightForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = CompostProductionWeight
        fields = ('weight', 'recorded', 'added_by', 'garden',)
        widgets = {
            'recorded': RecordedInput(),
        }


class CompostProductionVolumeForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = CompostProductionVolume
        fields = ('volume', 'recorded', 'added_by', 'garden',)
        widgets = {
            'recorded': RecordedInput(),
        }

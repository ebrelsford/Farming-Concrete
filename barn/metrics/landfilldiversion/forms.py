from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm

from farmingconcrete.models import Garden
from ..forms import RecordedInput
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class LandfillDiversionWeightForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = LandfillDiversionWeight
        fields = ('weight', 'recorded', 'added_by', 'garden',)
        widgets = {
            'recorded': RecordedInput(),
        }


class LandfillDiversionVolumeForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = LandfillDiversionVolume
        fields = ('volume', 'recorded', 'added_by', 'garden',)
        widgets = {
            'recorded': RecordedInput(),
        }

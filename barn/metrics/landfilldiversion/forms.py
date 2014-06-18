from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm

from farmingconcrete.models import Garden
from ..forms import RecordedField, RecordedInput
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class LandfillDiversionWeightForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    recorded = RecordedField(label='Date recorded', required=True)

    class Meta:
        model = LandfillDiversionWeight
        fields = ('recorded', 'weight', 'added_by', 'garden',)


class LandfillDiversionVolumeForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    recorded = RecordedField(label='Date recorded', required=True)

    class Meta:
        model = LandfillDiversionVolume
        fields = ('recorded', 'volume', 'added_by', 'garden',)

from django.contrib.auth.models import User
from django.forms import (HiddenInput, ModelChoiceField, ModelForm,
                          ValidationError)

from farmingconcrete.models import Garden
from ..forms import RecordedInput
from .models import RainwaterHarvest


class RainwaterHarvestForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    def clean(self):
        cleaned_data = super(RainwaterHarvestForm, self).clean()
        recorded_start = cleaned_data.get('recorded_start')
        recorded = cleaned_data.get('recorded')
        if recorded_start > recorded:
            raise ValidationError('Recorded start must come before recorded '
                                  'end')
        return cleaned_data

    class Meta:
        model = RainwaterHarvest
        fields = ('roof_length', 'roof_width', 'recorded_start', 'recorded',
                  'added_by', 'garden',)
        widgets = {
            'recorded_start': RecordedInput(),
            'recorded': RecordedInput(),
        }

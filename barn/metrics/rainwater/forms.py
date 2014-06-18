from django.forms import ValidationError

from ..forms import RecordedField, RecordForm
from .models import RainwaterHarvest


class RainwaterHarvestForm(RecordForm):
    recorded = RecordedField(label='End date')
    recorded_start = RecordedField(label='Start date')

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

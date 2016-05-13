from django.forms import HiddenInput, ValidationError

from ..forms import RecordedField, RecordForm
from .models import RainwaterHarvest
import decimal

from .utils import calculate_rainwater_gallons


class RainwaterHarvestForm(RecordForm):
    recorded = RecordedField(label='End date')
    recorded_start = RecordedField(label='Start date')

    def calculate_volume(self, garden=None, roof_length=0, roof_width=0,
                         recorded_start=None, recorded=None, **kwargs):
        gallons = calculate_rainwater_gallons(
            [garden.latitude, garden.longitude],
            float(roof_length),
            float(roof_width),
            recorded_start,
            recorded
        )

        # Round result to two decimals
        decimal_ctx = decimal.Context(prec=10, rounding=decimal.ROUND_HALF_UP)
        gallons = decimal_ctx.create_decimal(gallons).quantize(decimal.Decimal(10) ** - 2)
        return gallons

    def clean(self):
        cleaned_data = super(RainwaterHarvestForm, self).clean()
        recorded_start = cleaned_data.get('recorded_start')
        recorded = cleaned_data.get('recorded')
        if recorded_start > recorded:
            raise ValidationError('Recorded start must come before recorded '
                                  'end')

        # Actually try to calculate volume before moving on
        try:
            cleaned_data['volume'] = self.calculate_volume(**cleaned_data)
        except Exception:
            raise ValidationError('Failed to calculate the volume for the '
                                  'date range you selected. Sometimes this '
                                  'happens if the date range includes today. '
                                  'Try again with different dates?')
        return cleaned_data

    class Meta:
        model = RainwaterHarvest
        fields = ('roof_length', 'roof_width', 'recorded_start', 'recorded',
                  'added_by', 'garden', 'volume')
        widgets = {
            'volume': HiddenInput,
        }

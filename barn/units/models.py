from django_measurement.models import MeasurementField
from measurement.measures import Volume, Weight


class VolumeField(MeasurementField):
    def __init__(self, *args, **kwargs):
        kwargs['measurement'] = Volume
        kwargs['unit_choices'] = (
            ('l', 'liters'),
            ('us_g', 'gallons'),
        )
        super(VolumeField, self).__init__(*args, **kwargs)


class WeightField(MeasurementField):
    def __init__(self, *args, **kwargs):
        kwargs['measurement'] = Weight
        kwargs['unit_choices'] = (
            ('g', 'grams'),
            ('kg', 'kilograms'),
            ('oz', 'ounces'),
            ('lb', 'pounds'),
        )
        super(WeightField, self).__init__(*args, **kwargs)

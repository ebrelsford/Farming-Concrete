from django_measurement.models import MeasurementField
from measurement.measures import Distance, Volume, Weight


class DistanceField(MeasurementField):
    def __init__(self, *args, **kwargs):
        kwargs['measurement'] = Distance
        kwargs['unit_choices'] = (
            ('m', 'meters'),
            ('ft', 'feet'),
        )
        super(DistanceField, self).__init__(*args, **kwargs)


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

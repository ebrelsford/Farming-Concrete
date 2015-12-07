from django_measurement.models import MeasurementField
from measurement.measures import Weight


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

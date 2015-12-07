from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from units.convert import system_weight_units
from ..export import MetricDatasetMixin
from .models import CompostProductionVolume, CompostProductionWeight


class WeightDatasetMixin(object):

    def __init__(self, **kwargs):
        units = system_weight_units(kwargs.get('measurement_system', None))

        self.base_fields.update({
            'weight': Field(attribute='weight_%s' % units,
                            header='weight (%s)' % units)
        })
        self._meta.fields = ['weight',] + self._meta.fields
        if self._meta.field_order:
            self._meta.field_order = ('weight',) + self._meta.field_order
        else:
            self._meta.field_order = ('weight',)
        super(WeightDatasetMixin, self).__init__(**kwargs)

    class Meta:
        model = CompostProductionWeight


class WeightDataset(WeightDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicWeightDataset(WeightDatasetMixin, PublicMetricDatasetMixin,
                          ModelDataset):
    pass


class VolumeDatasetMixin():
    volume = Field(header='volume (gallons)')

    class Meta:
        model = CompostProductionVolume
        fields = ['volume',]


class VolumeDataset(VolumeDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicVolumeDataset(VolumeDatasetMixin, PublicMetricDatasetMixin,
                          ModelDataset):
    pass

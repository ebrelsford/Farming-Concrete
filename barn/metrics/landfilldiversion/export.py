from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from units.convert import system_volume_units, system_weight_units
from ..export import MetricDatasetMixin
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class WeightDatasetMixin(object):
    weight = Field(header='weight (pounds)')

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
        model = LandfillDiversionWeight


class WeightDataset(WeightDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicWeightDataset(WeightDatasetMixin, PublicMetricDatasetMixin,
                          ModelDataset):
    pass


class VolumeDatasetMixin(object):

    def __init__(self, **kwargs):
        units = system_volume_units(kwargs.get('measurement_system', None))

        self.base_fields.update({
            'volume': Field(attribute='volume_%s' % units,
                            header='volume (%s)' % units)
        })
        self._meta.fields = ['volume',] + self._meta.fields
        if self._meta.field_order:
            self._meta.field_order = ('volume',) + self._meta.field_order
        else:
            self._meta.field_order = ('volume',)
        super(VolumeDatasetMixin, self).__init__(**kwargs)

    class Meta:
        model = LandfillDiversionVolume


class VolumeDataset(VolumeDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicVolumeDataset(VolumeDatasetMixin, PublicMetricDatasetMixin,
                          ModelDataset):
    pass

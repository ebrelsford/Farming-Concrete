from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class WeightDatasetMixin(object):
    weight = Field(header='weight (pounds)')

    class Meta:
        model = LandfillDiversionWeight
        fields = ['weight',]


class WeightDataset(WeightDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicWeightDataset(WeightDatasetMixin, PublicMetricDatasetMixin,
                          ModelDataset):
    pass


class VolumeDatasetMixin(object):
    volume = Field(header='volume (gallons)')

    class Meta:
        model = LandfillDiversionVolume
        fields = ['volume',]


class VolumeDataset(VolumeDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicVolumeDataset(VolumeDatasetMixin, PublicMetricDatasetMixin,
                          ModelDataset):
    pass

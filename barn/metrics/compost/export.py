from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import CompostProductionVolume, CompostProductionWeight


class WeightDatasetMixin(object):
    weight = Field(header='weight (pounds)')

    class Meta:
        model = CompostProductionWeight
        fields = ['weight',]


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

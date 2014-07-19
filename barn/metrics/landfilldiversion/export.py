from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class WeightDataset(MetricDatasetMixin, ModelDataset):
    weight = Field(header='weight (pounds)')

    class Meta:
        model = LandfillDiversionWeight
        fields = ['weight',]


class VolumeDataset(MetricDatasetMixin, ModelDataset):
    volume = Field(header='volume (gallons)')

    class Meta:
        model = LandfillDiversionVolume
        fields = ['volume',]

from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import CompostProductionVolume, CompostProductionWeight


class WeightDataset(MetricDatasetMixin, ModelDataset):
    # TODO generate from the model's fields' labels?
    weight = Field(header='weight (pounds)')

    class Meta:
        model = CompostProductionWeight
        fields = ['weight',]


class VolumeDataset(MetricDatasetMixin, ModelDataset):
    volume = Field(header='volume (gallons)')

    class Meta:
        model = CompostProductionVolume
        fields = ['volume',]

from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import RainwaterHarvest


class RainwaterHarvestDataset(MetricDatasetMixin, ModelDataset):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')
    roof_length = Field(header='roof length (feet)')
    roof_width = Field(header='roof width (feet)')
    volume = Field(header='volume (gallons)')

    class Meta:
        model = RainwaterHarvest
        field_order = ('recorded_start', 'recorded', 'added_by_display',
                       'roof_length', 'roof_width', 'volume',)

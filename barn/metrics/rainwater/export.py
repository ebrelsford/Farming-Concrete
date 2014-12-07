from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import RainwaterHarvest


class RainwaterHarvestDatasetMixin(object):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')
    roof_length = Field(header='roof length (feet)')
    roof_width = Field(header='roof width (feet)')
    volume = Field(header='volume (gallons)')

    class Meta:
        model = RainwaterHarvest
        fields = [
            'recorded_start',
            'recorded',
            'roof_length',
            'roof_width',
            'volume',
        ]
        field_order = (
            'recorded_start',
            'recorded',
            'roof_length',
            'roof_width',
            'volume',
        )


class RainwaterHarvestDataset(RainwaterHarvestDatasetMixin, MetricDatasetMixin,
                              ModelDataset):
    pass


class PublicRainwaterHarvestDataset(RainwaterHarvestDatasetMixin,
                                    PublicMetricDatasetMixin, ModelDataset):
    pass

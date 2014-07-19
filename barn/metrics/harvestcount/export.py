from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import Harvest


class HarvestcountDataset(MetricDatasetMixin, ModelDataset):
    gardener = Field(header='gardener')
    crop = Field(header='crop')
    crop_variety = Field(header='crop variety')
    weight = Field(header='weight')
    plants = Field(header='plants')
    area = Field(header='area')

    class Meta:
        model = Harvest
        field_order = (
            'recorded',
            'added_by_display',
            'gardener',
            'crop',
            'crop_variety',
            'weight',
            'plants',
            'area',
        )

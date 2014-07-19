from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import Patch


class CropcountDataset(MetricDatasetMixin, ModelDataset):
    recorded = Field(header='recorded')
    bed = Field(header='bed')
    crop = Field(header='crop')
    crop_variety = Field(header='crop variety')
    quantity = Field(header='quantity')
    units = Field(header='units')

    class Meta:
        model = Patch
        field_order = (
            'recorded',
            'added_by_display',
            'bed',
            'crop',
            'crop_variety',
            'quantity',
            'units',
        )

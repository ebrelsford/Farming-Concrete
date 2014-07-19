from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import YumYuck


class YumYuckDataset(MetricDatasetMixin, ModelDataset):
    recorded = Field(header='recorded')
    crop = Field(header='crop')
    yum_before = Field(header='yum before')
    yuck_before = Field(header='yuck before')
    yum_after = Field(header='yum after')
    yuck_after = Field(header='yuck after')

    class Meta:
        model = YumYuck
        field_order = (
            'recorded',
            'added_by_display',
            'crop',
            'yum_before',
            'yuck_before',
            'yum_after',
            'yuck_after',
        )

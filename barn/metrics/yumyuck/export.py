from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import YumYuck


class YumYuckDatasetMixin(object):
    recorded = Field(header='recorded')
    crop = Field(header='crop')
    yum_before = Field(header='yum before')
    yuck_before = Field(header='yuck before')
    yum_after = Field(header='yum after')
    yuck_after = Field(header='yuck after')

    class Meta:
        model = YumYuck
        fields = [
            'recorded',
            'crop',
            'yum_before',
            'yuck_before',
            'yum_after',
            'yuck_after',
        ]
        field_order = (
            'recorded',
            'crop',
            'yum_before',
            'yuck_before',
            'yum_after',
            'yuck_after',
        )


class YumYuckDataset(YumYuckDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicYumYuckDataset(YumYuckDatasetMixin, PublicMetricDatasetMixin,
                           ModelDataset):
    pass

from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import LookingGoodEvent


class LookingGoodDatasetMixin(object):
    total_participants = Field(header='total participants')
    total_tags = Field(header='total tags')
    items_tagged = Field(header='items tagged')

    class Meta:
        model = LookingGoodEvent
        fields = [
            'total_participants',
            'total_tags',
            'items_tagged',
        ]


class LookingGoodDataset(LookingGoodDatasetMixin, MetricDatasetMixin,
                         ModelDataset):
    pass


class PublicLookingGoodDataset(LookingGoodDatasetMixin,
                               PublicMetricDatasetMixin, ModelDataset):
    pass

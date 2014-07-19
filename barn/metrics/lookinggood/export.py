from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import LookingGoodEvent


class LookingGoodDataset(MetricDatasetMixin, ModelDataset):
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

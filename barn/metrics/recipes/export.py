from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import RecipeTally


class RecipeTallyDatasetMixin(object):
    recorded = Field(header='recorded end')
    recipes_count = Field(header='# of recipes')

    class Meta:
        model = RecipeTally
        fields = [
            'recorded',
            'recipes_count',
        ]
        field_order = (
            'recorded',
            'recipes_count',
        )


class RecipeTallyDataset(RecipeTallyDatasetMixin, MetricDatasetMixin,
                         ModelDataset):
    pass


class PublicRecipeTallyDataset(RecipeTallyDatasetMixin,
                               PublicMetricDatasetMixin, ModelDataset):
    pass

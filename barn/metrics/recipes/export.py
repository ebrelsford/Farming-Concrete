from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import RecipeTally


class RecipeTallyDataset(MetricDatasetMixin, ModelDataset):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')
    recipes_count = Field(header='# of recipes')

    class Meta:
        model = RecipeTally
        field_order = (
            'recorded_start',
            'recorded',
            'added_by_display',
            'recipes_count',
        )

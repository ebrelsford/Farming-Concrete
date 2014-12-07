from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class RecipeTallyQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'recipes_count',
            'recorded_start',
        )
        return self.values(*values_args)


class RecipeTallyManager(MetricManager):
    
    def get_queryset(self):
        return RecipeTallyQuerySet(self.model)


class RecipeTally(BaseMetricRecord):
    objects = RecipeTallyManager()
    recorded_start = models.DateField(_('recorded start'))
    recipes_count = models.PositiveIntegerField(_('# of recipes'))

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(RecipeTally, cls).get_summarize_kwargs()
        kwargs.update({
            'recipes_count': Sum('recipes_count'),
        })
        return kwargs


from .export import RecipeTallyDataset, PublicRecipeTallyDataset


register('Healthy Eating', {
    'add_record_template': 'metrics/recipes/tally/add_record.html',
    'all_gardens_url_name': 'recipes_tally_all_gardens',
    'model': RecipeTally,
    'number': 3,
    'garden_detail_url_name': 'recipes_tally_garden_details',
    'group': 'Health Data',
    'group_number': 3,
    'index_url_name': 'recipes_tally_index',
    'short_name': 'tally',
    'dataset': RecipeTallyDataset,
    'public_dataset': PublicRecipeTallyDataset,
})

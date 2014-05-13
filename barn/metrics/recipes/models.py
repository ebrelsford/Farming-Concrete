from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class RecipeTally(BaseMetricRecord):

    recorded_start = models.DateField(_('recorded start'),
        help_text=_('The beginning of the date range for this record'),
    )

    recipes_count = models.PositiveIntegerField(_('# of recipes'),
        help_text=_('The number of recipes counted'),
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(RecipeTally, cls).get_summarize_kwargs()
        kwargs.update({
            'recipes_count': Sum('recipes_count'),
        })
        return kwargs


register('Healthy Eating', {
    'add_record_template': 'metrics/recipes/tally/add_record.html',
    'all_gardens_url_name': 'recipes_tally_all_gardens',
    'download_url_name': 'recipes_tally_garden_csv',
    'model': RecipeTally,
    'number': 3,
    'garden_detail_url_name': 'recipes_tally_garden_details',
    'group': 'Health Data',
    'group_number': 3,
    'index_url_name': 'recipes_tally_index',
    'summarize_template': 'metrics/recipes/tally/summarize.html',
    'user_gardens_url_name': 'recipes_tally_user_gardens',
})

from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class RecipesConfig(MetricConfig):
    label = 'recipes'
    name = 'metrics.recipes'

    def get_metric_models(self):
        return [self.get_model(c) for c in ('RecipeTally',)]

    def ready(self):
        super(RecipesConfig, self).ready()

        from .export import RecipeTallyDataset, PublicRecipeTallyDataset

        register('Healthy Eating', {
            'add_record_template': 'metrics/recipes/tally/add_record.html',
            'all_gardens_url_name': 'recipes_tally_all_gardens',
            'model': self.get_model('RecipeTally'),
            'number': 3,
            'garden_detail_url_name': 'recipes_tally_garden_details',
            'group': 'Health Data',
            'group_number': 3,
            'index_url_name': 'recipes_tally_index',
            'short_name': 'tally',
            'dataset': RecipeTallyDataset,
            'public_dataset': PublicRecipeTallyDataset,
            'description': _('Community gardens and urban farms make freshly picked '
                             'produce accessible and affordable for city dwellers. '
                             'Discovering how people use garden-grown produce in '
                             'their kitchens can influence what gets planted each '
                             'year. This method helps you record all the recipes '
                             'that were created using your garden produce, and the '
                             'report measures the number of recipes shared in a '
                             'specified period.'),
        })

from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class HarvestcountConfig(MetricConfig):
    label = 'harvestcount'
    name = 'metrics.harvestcount'

    def get_metric_models(self):
        return [self.get_model(c) for c in ('Harvest',)]

    def ready(self):
        super(HarvestcountConfig, self).ready()

        from .export import HarvestcountDataset, PublicHarvestcountDataset

        register('Harvest Count', {
            'all_gardens_url_name': 'harvestcount_all_gardens',
            'download_url_name': 'harvestcount_download_garden_harvestcount_as_csv',
            'model': self.get_model('Harvest'),
            'number': 2,
            'garden_detail_url_name': 'harvestcount_garden_details',
            'group': 'Food Production Data',
            'group_number': 0,
            'index_url_name': 'harvestcount_index',
            'dataset': HarvestcountDataset,
            'public_dataset': PublicHarvestcountDataset,
            'description': _('This report tallies up all of the pounds of produce '
                             'harvested in your garden this year. Keeping track of '
                             'your produce helps you quantify the wealth of fruits '
                             'and vegetables grown in your garden.'),
            'chart': {
                'y': 'weight_new',
            },
        })

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register


class RainwaterConfig(AppConfig):
    label = 'rainwater'
    name = 'metrics.rainwater'

    def ready(self):
        from .export import (RainwaterHarvestDataset,
                             PublicRainwaterHarvestDataset)

        register('Rainwater Harvesting', {
            'add_record_label': 'Add rainwater harvesting',
            'model': self.get_model('RainwaterHarvest'),
            'number': 3,
            'garden_detail_url_name': 'rainwater_harvest_garden_details',
            'group': 'Environmental Data',
            'group_number': 1,
            'index_url_name': 'rainwater_harvest_index',
            'short_name': 'harvest',
            'dataset': RainwaterHarvestDataset,
            'public_dataset': PublicRainwaterHarvestDataset,
            'description': _('This report utilizes rainfall data from local weather '
                             'stations to measure the total gallons of rainwater your '
                             'garden harvested for a specified period (top graph) and '
                             'for the whole period you\'ve been collecting this data '
                             '(bottom graph).'),
        })

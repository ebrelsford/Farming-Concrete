from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class CompostConfig(MetricConfig):
    label = 'compost'
    name = 'metrics.compost'

    def get_metric_models(self):
        return [self.get_model(c) for c in ('CompostProductionWeight',
                                            'CompostProductionVolume',)]

    def ready(self):
        super(CompostConfig, self).ready()

        from .export import (VolumeDataset, WeightDataset, PublicVolumeDataset,
                             PublicWeightDataset)

        register('Compost Production by Weight', {
            'add_record_label': 'Add compost by weight',
            'all_gardens_url_name': 'compostproduction_weight_all_gardens',
            'model': self.get_model('CompostProductionWeight'),
            'number': 2,
            'garden_detail_url_name': 'compostproduction_weight_garden_details',
            'group': 'Environmental Data',
            'group_number': 1,
            'index_url_name': 'compostproduction_weight_index',
            'short_name': 'weight',
            'dataset': WeightDataset,
            'public_dataset': PublicWeightDataset,
            'description': _('This report measures the weight of compost your garden '
                             'produced in a specified time period (top graph) and for '
                             'the whole period you\'ve been collecting this data '
                             '(bottom graph).  Knowing how much compost your garden '
                             'produces measures your garden\'s positive environmental '
                             'impact, and can help you plan for regular soil '
                             'improvements.'),
        })

        register('Compost Production by Volume', {
            'add_record_label': 'Add compost by volume',
            'all_gardens_url_name': 'compostproduction_volume_all_gardens',
            'model': self.get_model('CompostProductionVolume'),
            'number': 2,
            'garden_detail_url_name': 'compostproduction_volume_garden_details',
            'group': 'Environmental Data',
            'group_number': 1,
            'index_url_name': 'compostproduction_volume_index',
            'short_name': 'volume',
            'dataset': VolumeDataset,
            'public_dataset': PublicVolumeDataset,
            'description': _('This report measures the volume of compost your garden '
                             'produced in a specified time period (top graph) and for '
                             'the whole period you\'ve been collecting this data '
                             '(bottom graph).  Knowing how much compost your garden '
                             'produces measures your garden\'s positive environmental '
                             'impact, and can help you plan for regular soil '
                             'improvements.'),
        })

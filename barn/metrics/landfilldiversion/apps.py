from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register


class LandfillDiversionConfig(AppConfig):
    label = 'landfilldiversion'
    name = 'metrics.landfilldiversion'

    def ready(self):
        from .export import (VolumeDataset, PublicVolumeDataset, WeightDataset,
                             PublicWeightDataset)

        register('Landfill Waste Diversion by Weight', {
            'add_record_label': 'Add landfill diversion by weight',
            'all_gardens_url_name': 'landfilldiversion_weight_all_gardens',
            'model': self.get_model('LandfillDiversionWeight'),
            'number': 1,
            'garden_detail_url_name': 'landfilldiversion_weight_garden_details',
            'group': 'Environmental Data',
            'group_number': 1,
            'index_url_name': 'landfilldiversion_weight_index',
            'short_name': 'weight',
            'dataset': WeightDataset,
            'public_dataset': PublicWeightDataset,
            'description': _('This report displays the total pounds of trash your '
                             'garden prevented from going into a landfill by turning '
                             'it into compost instead. Garden composting helps divert '
                             'a significant amount of waste that would have gone into '
                             'the landfill waste stream. Calculating the weight of '
                             'waste diverted measures your garden\'s positive '
                             'environmental impact. The top graph shows waste '
                             'diverted for specified time period, and the bottom '
                             'graph shows the total gallons diverted since you '
                             'started collecting data.'),
        })

        register('Landfill Waste Diversion by Volume', {
            'add_record_label': 'Add landfill diversion by volume',
            'all_gardens_url_name': 'landfilldiversion_volume_all_gardens',
            'model': self.get_model('LandfillDiversionVolume'),
            'number': 1,
            'garden_detail_url_name': 'landfilldiversion_volume_garden_details',
            'group': 'Environmental Data',
            'group_number': 1,
            'index_url_name': 'landfilldiversion_volume_index',
            'short_name': 'volume',
            'dataset': VolumeDataset,
            'public_dataset': PublicVolumeDataset,
            'description': _('This report displays the total gallons of trash '
                             'prevented from going into a landfill by turning it into '
                             'compost instead. Garden composting helps divert a '
                             'significant amount of waste that would have gone into '
                             'the landfill waste stream. Calculating the volume of '
                             'waste diverted measures your garden\'s positive '
                             'environmental impact. The top graph shows waste '
                             'diverted for specified time period, and the bottom '
                             'graph shows the total gallons diverted since you '
                             'started collecting data.'),
        })

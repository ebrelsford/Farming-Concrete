from django.apps import AppConfig
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ..registry import register


class CropcountConfig(AppConfig):
    label = 'cropcount'
    name = 'metrics.cropcount'

    def ready(self):
        from .export import CropcountDataset, PublicCropcountDataset

        register('Crop Count', {
            'all_gardens_url_name': 'cropcount_all_gardens',
            'bed_content_type': ContentType.objects.get_for_model(self.get_model('Box')),
            'model': self.get_model('Patch'),
            'number': 1,
            'garden_detail_url_name': 'cropcount_garden_details',
            'group': 'Food Production Data',
            'group_number': 0,
            'index_url_name': 'cropcount_index',
            'dataset': CropcountDataset,
            'public_dataset': PublicCropcountDataset,
            'description': _('Keeping track of your crop count helps you get a handle '
                             'on the annual productivity of your garden. This report '
                             'displays total number of crops in a garden, and how '
                             'many plants of each crop type measure by bed, row feet '
                             'or square feet.'),
        })

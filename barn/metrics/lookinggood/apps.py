from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register
from .export import LookingGoodDataset, PublicLookingGoodDataset
from .models import LookingGoodEvent


class LookingGoodConfig(AppConfig):
    label = 'lookinggood'
    name = 'metrics.lookinggood'

    def ready(self):
        register('Beauty of the Garden', {
            'add_record_label': 'Add looking good tags',
            'add_record_template': 'metrics/lookinggood/event/add_record.html',
            'all_gardens_url_name': 'lookinggood_event_all_gardens',
            'model': LookingGoodEvent,
            'number': 4,
            'garden_detail_url_name': 'lookinggood_event_garden_details',
            'group': 'Health Data',
            'group_number': 3,
            'index_url_name': 'lookinggood_event_index',
            'short_name': 'event',
            'dataset': LookingGoodDataset,
            'public_dataset': PublicLookingGoodDataset,
            'description': _('Green spaces in the form of community gardens and urban '
                             'farms add to the beauty of neighborhoods. This protocol '
                             'will help you discover what everyone living near your '
                             'garden feels about its contribution to the community. '
                             'This report illustrates what visitors, volunteers and '
                             'members are attracted to in the garden.'),
        })

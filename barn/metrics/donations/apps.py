from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register
from .export import DonationDataset, PublicDonationDataset
from .models import Donation


class DonationsConfig(AppConfig):
    label = 'donations'
    name = 'metrics.donations'

    def ready(self):
        register('Donations of Food', {
            'add_record_label': 'Add donation of food',
            'model': Donation,
            'number': 2,
            'garden_detail_url_name': 'donations_garden_details',
            'group': 'Economic Data',
            'group_number': 4,
            'dataset': DonationDataset,
            'public_dataset': PublicDonationDataset,
            'description': _('Many community gardeners are motivated to grow fresh '
                             'and healthy vegetables for food banks, soup kitchens, '
                             'and other charitable organizations. In fact, some '
                             'gardens grow food with no other goal in mind. Tracking '
                             'the amount of food you donate can help pantries better '
                             'manage their weekly inventories. This report quantifies '
                             'the type and quantity of produce donated by your garden '
                             'in a specified period.')
        })

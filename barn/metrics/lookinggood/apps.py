from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class LookingGoodConfig(MetricConfig):
    label = 'lookinggood'
    name = 'metrics.lookinggood'

    def get_metric_models(self):
        return [self.get_model(c) for c in ('LookingGoodEvent',)]

    def ready(self):
        super(LookingGoodConfig, self).ready()

        from .export import LookingGoodDataset, PublicLookingGoodDataset

        register('Beauty of the Garden', {
            'add_record_label': 'Add looking good tags',
            'add_record_template': 'metrics/lookinggood/event/add_record.html',
            'all_gardens_url_name': 'lookinggood_event_all_gardens',
            'model': self.get_model('LookingGoodEvent'),
            'number': 4,
            'garden_detail_url_name': 'lookinggood_event_garden_details',
            'group': 'Health Data',
            'group_number': 3,
            'index_url_name': 'lookinggood_event_index',
            'short_name': 'event',
            'dataset': LookingGoodDataset,
            'public_dataset': PublicLookingGoodDataset,
            'description': _('Green spaces in the form of community gardens and urban '
                             'farms add to the beauty of neighborhoods. This method '
                             'will help you discover what everyone living near your '
                             'garden feels about its contribution to the community. '
                             'This report illustrates what visitors, volunteers and '
                             'members are attracted to in the garden.'),
        })

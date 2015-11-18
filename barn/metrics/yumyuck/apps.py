from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class YumYuckConfig(MetricConfig):
    label = 'yumyuck'
    name = 'metrics.yumyuck'

    def get_metric_models(self):
        return [self.get_model(c) for c in ('YumYuck',)]

    def ready(self):
        super(YumYuckConfig, self).ready()

        from .export import YumYuckDataset, PublicYumYuckDataset

        register('Changes in Attitude: Yum & Yuck', {
            'add_record_template': 'metrics/yumyuck/change/add_record.html',
            'all_gardens_url_name': 'yumyuck_change_all_gardens',
            'model': self.get_model('YumYuck'),
            'number': 1,
            'garden_detail_url_name': 'yumyuck_change_garden_details',
            'group': 'Health Data',
            'group_number': 3,
            'index_url_name': 'yumyuck_change_index',
            'short_name': 'change',
            'dataset': YumYuckDataset,
            'public_dataset': PublicYumYuckDataset,
            'description': _('Some community gardens and urban farms - particularly '
                             'those that feature programs for school-age youth - have '
                             'some sense of how they want to change attitudes about '
                             'eating fresh fruits and vegetables. This report '
                             'measures how many attitudes changed from negative to '
                             'positive about a particular vegetable after doing a '
                             'taste-test in the garden.'),
        })

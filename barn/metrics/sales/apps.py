from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class SalesConfig(MetricConfig):
    label = 'sales'
    name = 'metrics.sales'

    def get_metric_models(self):
        return [self.get_model('Sale'),]

    def ready(self):
        super(SalesConfig, self).ready()

        from .export import SaleDataset, PublicSaleDataset

        register('Market Sales', {
            'add_record_label': 'Add market sale',
            'model': self.get_model('Sale'),
            'number': 1,
            'garden_detail_url_name': 'sales_garden_details',
            'group': 'Economic Data',
            'group_number': 4,
            'dataset': SaleDataset,
            'public_dataset': PublicSaleDataset,
            'description': _('Making fresh vegetables accessible and affordable to '
                             'city-dwellers is one of the joys of urban gardening. '
                             'This method helps you track what you\'re selling, and '
                             'how much you\'re making, at local farmer\'s markets. '
                             'These results are powerful source of information for '
                             'adjusting what you choose to sell each week, or for '
                             'quantifying how your garden contributes to the local '
                             'economy.'),
        })

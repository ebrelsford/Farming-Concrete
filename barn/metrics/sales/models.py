from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class SaleQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'product',
            'unit',
            'units_sold',
            'total_price',
        )
        return self.values(*values_args)


class SaleManager(MetricManager):
    
    def get_queryset(self):
        return SaleQuerySet(self.model)


class Sale(BaseMetricRecord):
    objects = SaleManager()
    product = models.CharField(_('product'),
        max_length=100,
    )
    unit = models.CharField(_('unit'),
        max_length=50,
    )
    unit_price = models.DecimalField(_('unit price'),
        max_digits=10,
        decimal_places=2,
    )
    units_sold = models.DecimalField(_('units sold'),
        max_digits=10,
        decimal_places=2,
    )
    total_price = models.DecimalField(_('total price'),
        max_digits=10,
        decimal_places=2,
    )

    def __unicode__(self):
        return 'Sale (%d) %s' % (
            self.pk,
            self.garden,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(Sale, cls).get_summarize_kwargs()
        kwargs.update({
            'total_units': Sum('units_sold'),
            'total_price': Sum('total_price'),
        })
        return kwargs


from .export import SaleDataset, PublicSaleDataset


register('Market Sales', {
    'add_record_label': 'Add market sale',
    'model': Sale,
    'number': 1,
    'garden_detail_url_name': 'sales_garden_details',
    'group': 'Economic Data',
    'group_number': 4,
    'dataset': SaleDataset,
    'public_dataset': PublicSaleDataset,
    'description': _('Making fresh vegetables accessible and affordable to '
                     'city-dwellers is one of the joys of urban gardening. '
                     'This protocol helps you track what you\'re selling, and '
                     'how much you\'re making, at local farmer\'s markets. '
                     'These results are powerful source of information for '
                     'adjusting what you choose to sell each week, or for '
                     'quantifying how your garden contributes to the local '
                     'economy.'),
})

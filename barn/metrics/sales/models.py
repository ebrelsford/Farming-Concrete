from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class Sale(BaseMetricRecord):
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


register('Market Sales', {
    'add_record_label': 'Add market sale',
    'download_url_name': 'sales_garden_csv',
    'model': Sale,
    'number': 1,
    'garden_detail_url_name': 'sales_garden_details',
    'group': 'Economic Data',
    'group_number': 4,
})

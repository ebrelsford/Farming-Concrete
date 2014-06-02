from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class Donation(BaseMetricRecord):
    produce_name = models.CharField(_('produce name'),
        max_length=100,
    )
    pounds = models.DecimalField(_('pounds donated'),
        max_digits=10,
        decimal_places=2,
    )

    def __unicode__(self):
        return 'Donation (%d) %s %.2f pounds' % (
            self.pk,
            self.garden,
            self.pounds or 0,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(Donation, cls).get_summarize_kwargs()
        kwargs.update({
            'pounds': Sum('pounds'),
        })
        return kwargs


register('Donations of Food', {
    'add_record_label': 'Add donation of food',
    'download_url_name': 'donations_garden_csv',
    'model': Donation,
    'number': 2,
    'garden_detail_url_name': 'donations_garden_details',
    'group': 'Economic Data',
    'group_number': 4,
})

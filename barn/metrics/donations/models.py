from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class DonationQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'produce_name',
            'pounds',
        )
        return self.values(*values_args)


class DonationManager(MetricManager):
    
    def get_queryset(self):
        return DonationQuerySet(self.model)


class Donation(BaseMetricRecord):
    objects = DonationManager()
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


from .export import DonationDataset, PublicDonationDataset


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

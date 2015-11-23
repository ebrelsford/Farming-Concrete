from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


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
        return '%.2f pounds of donations' % (
            self.pounds or 0,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(Donation, cls).get_summarize_kwargs()
        kwargs.update({
            'pounds': Sum('pounds'),
        })
        return kwargs

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from units.convert import to_preferred_weight_units
from units.models import WeightField
from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class DonationQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'produce_name',
            'weight',
            'weight_units',
        )
        return self.extra(select={'weight_units': '\'g\''}).values(*values_args)


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
        blank=True,
        null=True,
    )
    weight = WeightField(blank=True, null=True)

    def __unicode__(self):
        try:
            return '%s of donations' % self.weight
        except Exception:
            return '%d' % self.pk

    @property
    def weight_kilograms(self):
        if not self.weight:
            return 0
        return self.weight.kg

    @property
    def weight_pounds(self):
        if not self.weight:
            return 0
        return self.weight.lb

    @property
    def weight_for_garden(self):
        """Convert weight to proper units for garden."""
        return to_preferred_weight_units(self.weight.value, self.garden,
                                         force_large_units=False)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(Donation, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight'),
        })
        return kwargs

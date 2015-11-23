from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class RainwaterHarvestQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'recorded_start',
            'volume',
        )
        return self.values(*values_args)


class RainwaterHarvestManager(MetricManager):
    
    def get_queryset(self):
        return RainwaterHarvestQuerySet(self.model)


class RainwaterHarvest(BaseMetricRecord):
    objects = RainwaterHarvestManager()
    roof_length = models.DecimalField(_('roof length (feet)'),
        max_digits=10,
        decimal_places=2
    )
    roof_width = models.DecimalField(_('roof width (feet)'),
        max_digits=10,
        decimal_places=2
    )
    volume = models.DecimalField(_('volume (gallons)'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    recorded_start = models.DateField(_('recorded start'),
        help_text=_('The beginning of the date range for this record'),
    )

    def __unicode__(self):
        return '%.2f gallons of rainwater harvested' % (
            self.volume or 0,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(RainwaterHarvest, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs

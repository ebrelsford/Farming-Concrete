from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


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
        return 'RainwaterHarvest (%d) %s %.2f gallons' % (
            self.pk,
            self.garden,
            self.volume or 0,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(RainwaterHarvest, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs


from .export import RainwaterHarvestDataset, PublicRainwaterHarvestDataset


register('Rainwater Harvesting', {
    'add_record_label': 'Add rainwater harvesting',
    'model': RainwaterHarvest,
    'number': 3,
    'garden_detail_url_name': 'rainwater_harvest_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'rainwater_harvest_index',
    'short_name': 'harvest',
    'dataset': RainwaterHarvestDataset,
    'public_dataset': PublicRainwaterHarvestDataset,
    'description': _('This report utilizes rainfall data from local weather '
                     'stations to measure the total gallons of rainwater your '
                     'garden harvested for a specified period (top graph) and '
                     'for the whole period you\'ve been collecting this data '
                     '(bottom graph).'),
})

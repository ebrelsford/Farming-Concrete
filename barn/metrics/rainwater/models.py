from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class RainwaterHarvest(BaseMetricRecord):
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


from .export import RainwaterHarvestDataset


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
})

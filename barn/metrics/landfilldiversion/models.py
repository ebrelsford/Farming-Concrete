from django.db import models
from django.db.models import Sum

from ..models import BaseMetricRecord
from ..registry import register


class LandfillDiversionWeight(BaseMetricRecord):
    weight = models.DecimalField('weight (pounds)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return 'LandfillDiversionWeight (%d) %s %.2f pounds' % (
            self.pk,
            self.garden,
            self.weight,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LandfillDiversionWeight, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight'),
        })
        return kwargs


class LandfillDiversionVolume(BaseMetricRecord):
    volume = models.DecimalField('volume (gallons)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return 'LandfillDiversionWeight (%d) %s %.2f gallons' % (
            self.pk,
            self.garden,
            self.volume,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LandfillDiversionVolume, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs


register('Landfill Diversion by Weight', {
    'all_gardens_url_name': 'landfilldiversion_weight_all_gardens',
    'model': LandfillDiversionWeight,
    'garden_detail_url_name': 'landfilldiversion_weight_garden_details',
    'group': 'Compost',
    'index_url_name': 'landfilldiversion_weight_index',
    'summarize_template': 'metrics/landfilldiversion/weight/summarize.html',
    'user_gardens_url_name': 'landfilldiversion_weight_user_gardens',
})


register('Landfill Diversion by Volume', {
    'all_gardens_url_name': 'landfilldiversion_volume_all_gardens',
    'model': LandfillDiversionVolume,
    'garden_detail_url_name': 'landfilldiversion_volume_garden_details',
    'group': 'Compost',
    'index_url_name': 'landfilldiversion_volume_index',
    'summarize_template': 'metrics/landfilldiversion/volume/summarize.html',
    'user_gardens_url_name': 'landfilldiversion_volume_user_gardens',
})

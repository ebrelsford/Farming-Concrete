from django.db import models
from django.db.models import Count, Max, Min, Sum

from ..models import BaseMetricRecord
from ..registry import register


class CompostProductionWeight(BaseMetricRecord):
    weight = models.DecimalField('weight (pounds)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return 'CompostProductionWeight (%d) %s %.2f pounds' % (
            self.pk,
            self.garden,
            self.weight,
        )

    @classmethod
    def summarize(cls, records):
        if not records:
            return None
        return records.aggregate(count=Count('pk'), weight=Sum('weight'),
                                 recorded_min=Min('recorded'),
                                 recorded_max=Max('recorded'))


class CompostProductionVolume(BaseMetricRecord):
    volume = models.DecimalField('volume (gallons)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return 'CompostProductionWeight (%d) %s %.2f gallons' % (
            self.pk,
            self.garden,
            self.volume,
        )

    @classmethod
    def summarize(cls, records):
        if not records:
            return None
        return records.aggregate(count=Count('pk'), volume=Sum('volume'),
                                 recorded_min=Min('recorded'),
                                 recorded_max=Max('recorded'))


register('Compost Production by Weight', {
    'model': CompostProductionWeight,
    'garden_detail_url_name': 'compostproduction_weight_garden_details',
    'group': 'Compost',
    'index_url_name': 'compostproduction_weight_index',
    'summarize_template': 'metrics/compost/weight/summarize.html',
})


register('Compost Production by Volume', {
    'model': CompostProductionVolume,
    'garden_detail_url_name': 'compostproduction_volume_garden_details',
    'group': 'Compost',
    'index_url_name': 'compostproduction_volume_index',
    'summarize_template': 'metrics/compost/volume/summarize.html',
})

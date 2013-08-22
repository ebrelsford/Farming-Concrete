from django.db import models
from django.db.models import Count, Max, Min, Sum

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
    def summarize(cls, records):
        if not records:
            return None
        return records.aggregate(count=Count('pk'), weight=Sum('weight'),
                                 recorded_min=Min('recorded'),
                                 recorded_max=Max('recorded'))


register('Landfill Diversion by Weight', {
    'model': LandfillDiversionWeight,
    'garden_detail_url_name': 'landfilldiversion_weight_garden_details',
    'index_url_name': 'landfilldiversion_weight_index',
})

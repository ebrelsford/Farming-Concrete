from django.db import models
from django.db.models import Sum

from audit.models import AuditedModel
from farmingconcrete.models import Garden, Variety
from ..models import BaseMetricRecord
from ..registry import register


class Gardener(AuditedModel):
    garden = models.ForeignKey(Garden)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Harvest(BaseMetricRecord):
    gardener = models.ForeignKey(Gardener)
    variety = models.ForeignKey(Variety)

    weight = models.DecimalField('weight (pounds)', max_digits=6,
                                 decimal_places=2)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=4, decimal_places=2, null=True,
                               blank=True)

    harvested = models.DateField(blank=True, null=True)
    reportable = models.BooleanField(default=True)

    def __unicode__(self):
        return "Harvest (%d) %s, %.2f pounds of %s" % (
            self.id,
            self.gardener.name,
            self.weight,
            self.variety.name,
        )

    @classmethod
    def summarize(cls, harvests):
        if not harvests:
            return None
        return {
            'harvests': harvests.order_by('harvested', 'gardener__name'),
            'weight': harvests.aggregate(t=Sum('weight'))['t'],
            'plant_types': harvests.values('variety__id').distinct().count(),
        }


register('Harvest Count', {
    'all_gardens_url_name': 'harvestcount_all_gardens',
    'model': Harvest,
    'garden_detail_url_name': 'harvestcount_garden_details',
    'group': 'Food Production',
    'index_url_name': 'harvestcount_index',
    'user_gardens_url_name': 'harvestcount_user_gardens',
})

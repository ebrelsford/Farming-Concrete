from django.db import models
from django.db.models import Sum

from audit.models import AuditedModel
from farmingconcrete.models import Garden
from ..models import BaseMetricRecord
from ..registry import register


class Gardener(AuditedModel):
    garden = models.ForeignKey(Garden)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Harvest(BaseMetricRecord):
    gardener = models.ForeignKey(Gardener)

    crop = models.ForeignKey('crops.Crop', null=True)
    crop_variety = models.ForeignKey('crops.Variety', blank=True, null=True)

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
            self.crop.name,
        )

    def get_crop_variety_display(self):
        if self.crop_variety:
            return self.crop_variety.name
        else:
            return None

    @classmethod
    def summarize(cls, harvests):
        if not harvests:
            return None
        return {
            'count': harvests.count(),
            'harvests': harvests.order_by('harvested', 'gardener__name'),
            'weight': harvests.aggregate(t=Sum('weight'))['t'],
            'plant_types': harvests.values('crop__id').distinct().count(),
            'recorded_max': harvests.aggregate(models.Max('recorded'))['recorded__max'],
        }


from .export import HarvestcountDataset


register('Harvest Count', {
    'all_gardens_url_name': 'harvestcount_all_gardens',
    'download_url_name': 'harvestcount_download_garden_harvestcount_as_csv',
    'model': Harvest,
    'number': 2,
    'garden_detail_url_name': 'harvestcount_garden_details',
    'group': 'Food Production Data',
    'group_number': 0,
    'index_url_name': 'harvestcount_index',
    'dataset': HarvestcountDataset,
})

from django.db import models
from django.db.models import Sum

from audit.models import AuditedModel
from farmingconcrete.models import Garden
from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class Gardener(AuditedModel):
    garden = models.ForeignKey(Garden)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class HarvestCountQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'crop__name',
            'crop_variety__name',
            'plants',
            'weight',
        )
        return self.values(*values_args)


class HarvestCountManager(MetricManager):
    
    def get_queryset(self):
        return HarvestCountQuerySet(self.model)


class Harvest(BaseMetricRecord):
    objects = HarvestCountManager()
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
        return "%.2f harvested pounds of %s" % (
            self.weight,
            self.crop.name,
        )

    def get_crop_variety_display(self):
        if self.crop_variety:
            return self.crop_variety.name
        else:
            return None

    def _garden_pk(self):
        """Get garden pk, convenient for exporting"""
        return self.gardener.garden.pk
    garden_pk = property(_garden_pk)

    def _garden_state(self):
        """Get garden state, convenient for exporting"""
        return self.gardener.garden.state
    garden_state = property(_garden_state)

    def _garden_zip(self):
        """Get garden state, convenient for exporting"""
        return self.gardener.garden.zip
    garden_zip = property(_garden_zip)

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

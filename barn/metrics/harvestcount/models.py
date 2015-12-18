from django.db import models
from django.db.models import Sum

from audit.models import AuditedModel
from farmingconcrete.models import Garden
from units.convert import to_preferred_weight_units, to_weight_units
from units.models import WeightField
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
            'weight_new',
            'weight_new_units',
        )
        return self.extra(select={'weight_new_units': '\'g\''}).values(*values_args)


class HarvestCountManager(MetricManager):
    
    def get_queryset(self):
        return HarvestCountQuerySet(self.model)


class Harvest(BaseMetricRecord):
    objects = HarvestCountManager()
    gardener = models.ForeignKey(Gardener)

    crop = models.ForeignKey('crops.Crop', null=True)
    crop_variety = models.ForeignKey('crops.Variety', blank=True, null=True)

    weight = models.DecimalField('weight (pounds)', max_digits=6,
                                 decimal_places=2, blank=True, null=True)
    weight_new = WeightField(blank=True, null=True)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=4, decimal_places=2, null=True,
                               blank=True)

    harvested = models.DateField(blank=True, null=True)
    reportable = models.BooleanField(default=True)

    def __unicode__(self):
        try:
            return "%s harvested of %s" % (
                self.weight_new,
                self.crop.name,
            )
        except Exception:
            return '%d' % self.pk

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

    @property
    def weight_kilograms(self):
        if not self.weight_new:
            return 0
        return self.weight_new.kg

    @property
    def weight_pounds(self):
        if not self.weight_new:
            return 0
        return self.weight_new.lb

    @property
    def weight_for_garden(self):
        """Convert weight to proper units for garden."""
        if self.garden:
            return to_preferred_weight_units(self.weight_new.value,
                                             self.garden,
                                             force_large_units=False)
        else:
            return to_weight_units(self.weight_new.value, 'imperial',
                                   force_large_units=False)


    @classmethod
    def summarize(cls, harvests):
        if not harvests:
            return None
        return {
            'count': harvests.count(),
            'harvests': harvests.order_by('harvested', 'gardener__name'),
            'weight': harvests.aggregate(t=Sum('weight_new'))['t'],
            'plant_types': harvests.values('crop__id').distinct().count(),
            'recorded_max': harvests.aggregate(models.Max('recorded'))['recorded__max'],
        }

from django.db import models

from farmingconcrete.models import GardenType, Variety


class Estimate(models.Model):
    estimated = models.DateField()
    notes = models.TextField(null=True, blank=True)
    should_be_used = models.BooleanField(default=True)
    valid_start = models.DateField()
    valid_end = models.DateField()
    garden_type = models.ForeignKey(GardenType, null=True, blank=True)

    class Meta:
        abstract = True


class VarietyEstimate(Estimate):
    variety = models.ForeignKey(Variety)

    crop = models.ForeignKey('crops.Crop', blank=True, null=True)
    crop_variety = models.ForeignKey('crops.Variety', blank=True, null=True)

    class Meta:
        abstract = True


class EstimatedYield(VarietyEstimate):
    pounds_per_plant = models.DecimalField(max_digits=6, decimal_places=2)


class EstimatedCost(VarietyEstimate):
    cost_per_pound = models.DecimalField(max_digits=6, decimal_places=2)
    organic = models.BooleanField(default=True)

    source = models.TextField(null=True, blank=True)

from django.db import models
from django.db.models import Sum

from units.convert import to_preferred_weight_units
from units.models import WeightField
from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class LandfillDiversionWeightQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'weight_new',
            'weight_new_units',
        )
        return self.extra(select={'weight_new_units': '\'g\''}).values(*values_args)


class LandfillDiversionWeightManager(MetricManager):
    
    def get_queryset(self):
        return LandfillDiversionWeightQuerySet(self.model)


class LandfillDiversionWeight(BaseMetricRecord):
    objects = LandfillDiversionWeightManager()
    weight = models.DecimalField('weight (pounds)',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_new = WeightField(blank=True, null=True)

    def __unicode__(self):
        try:
            return '%s of landfill diversion' % self.weight_new
        except Exception:
            return '%d' % self.pk

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
        try:
            return to_preferred_weight_units(self.weight_new.value,
                                             self.garden,
                                             force_large_units=False)
        except AttributeError:
            return None

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LandfillDiversionWeight, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight_new'),
        })
        return kwargs


class LandfillDiversionVolumeQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'volume',
        )
        return self.values(*values_args)


class LandfillDiversionVolumeManager(MetricManager):
    
    def get_queryset(self):
        return LandfillDiversionVolumeQuerySet(self.model)


class LandfillDiversionVolume(BaseMetricRecord):
    objects = LandfillDiversionVolumeManager()
    volume = models.DecimalField('volume (gallons)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return '%.2f gallons of landfill diversion' % (self.volume,)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LandfillDiversionVolume, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs

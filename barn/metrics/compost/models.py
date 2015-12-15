from django.db import models
from django.db.models import Sum

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from units.convert import to_preferred_volume_units, to_preferred_weight_units
from units.models import VolumeField, WeightField


class CompostProductionWeightQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + ('weight', 'weight_units')
        return self.extra(select={'weight_units': '\'g\''}).values(*values_args)


class CompostProductionWeightManager(MetricManager):
    
    def get_queryset(self):
        return CompostProductionWeightQuerySet(self.model)


class CompostProductionWeight(BaseMetricRecord):
    objects = CompostProductionWeightManager()

    weight = WeightField()

    def __unicode__(self):
        try:
            return '%s of compost' % self.weight
        except Exception:
            return '%d' % self.pk

    @property
    def weight_kilograms(self):
        if not self.weight:
            return 0
        return self.weight.kg

    @property
    def weight_pounds(self):
        if not self.weight:
            return 0
        return self.weight.lb

    @property
    def weight_for_garden(self):
        """Convert weight to proper units for garden."""
        return to_preferred_weight_units(self.weight.value, self.garden,
                                         force_large_units=False)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(CompostProductionWeight, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight'),
        })
        return kwargs


class CompostProductionVolumeQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + ('volume_new',
                                                      'volume_new_units',)
        return self.extra(select={
            'volume_new': '1000 * volume_new',
            'volume_new_units': '\'liter\'',
        }).values(*values_args)


class CompostProductionVolumeManager(MetricManager):
    
    def get_queryset(self):
        return CompostProductionVolumeQuerySet(self.model)


class CompostProductionVolume(BaseMetricRecord):
    objects = CompostProductionVolumeManager()
    volume = models.DecimalField('volume (gallons)',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    volume_new = VolumeField(blank=True, null=True)

    def __unicode__(self):
        try:
            return '%s of compost' % self.volume_new
        except Exception:
            return '%d' % self.pk

    @property
    def volume_liters(self):
        if not self.volume_new:
            return 0
        return self.volume_new.l

    @property
    def volume_gallons(self):
        if not self.volume_new:
            return 0
        return self.volume_new.us_g

    @property
    def volume_for_garden(self):
        """Convert volume to proper units for garden."""
        try:
            return to_preferred_volume_units(self.garden,
                                             liters=self.volume_new.value,
                                             force_large_units=False)
        except AttributeError:
            return None

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(CompostProductionVolume, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume_new'),
        })
        return kwargs

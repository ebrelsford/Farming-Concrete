from django.db import models
from django.db.models import Sum

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from units.convert import to_preferred_weight_units
from units.models import WeightField


class CompostProductionWeightQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + ('weight_new', 'weight_new_units')
        return self.extra(select={'weight_new_units': '\'g\''}).values(*values_args)


class CompostProductionWeightManager(MetricManager):
    
    def get_queryset(self):
        return CompostProductionWeightQuerySet(self.model)


class CompostProductionWeight(BaseMetricRecord):
    objects = CompostProductionWeightManager()
    weight = models.DecimalField('weight (pounds)',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    weight_new = WeightField(blank=True, null=True)

    def __unicode__(self):
        try:
            return '%s of compost' % self.weight_new
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
        return to_preferred_weight_units(self.weight_new.value, self.garden,
                                         force_large_units=False)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(CompostProductionWeight, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight_new'),
        })
        return kwargs


class CompostProductionVolumeQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + ('volume',)
        return self.values(*values_args)


class CompostProductionVolumeManager(MetricManager):
    
    def get_queryset(self):
        return CompostProductionVolumeQuerySet(self.model)


class CompostProductionVolume(BaseMetricRecord):
    objects = CompostProductionVolumeManager()
    volume = models.DecimalField('volume (gallons)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return '%.2f gallons of compost' % (self.volume,)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(CompostProductionVolume, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs

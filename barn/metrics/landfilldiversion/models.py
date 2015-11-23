from django.db import models
from django.db.models import Sum

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class LandfillDiversionWeightQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'weight',
        )
        return self.values(*values_args)


class LandfillDiversionWeightManager(MetricManager):
    
    def get_queryset(self):
        return LandfillDiversionWeightQuerySet(self.model)


class LandfillDiversionWeight(BaseMetricRecord):
    objects = LandfillDiversionWeightManager()
    weight = models.DecimalField('weight (pounds)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return '%.2f pounds of landfill diversion' % (self.weight,)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LandfillDiversionWeight, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight'),
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

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class CompostProductionWeightQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + ('weight',)
        return self.values(*values_args)


class CompostProductionWeightManager(MetricManager):
    
    def get_queryset(self):
        return CompostProductionWeightQuerySet(self.model)


class CompostProductionWeight(BaseMetricRecord):
    objects = CompostProductionWeightManager()
    weight = models.DecimalField('weight (pounds)',
        max_digits=8,
        decimal_places=2
    )

    def __unicode__(self):
        return 'CompostProductionWeight (%d) %s %.2f pounds' % (
            self.pk,
            self.garden,
            self.weight,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(CompostProductionWeight, cls).get_summarize_kwargs()
        kwargs.update({
            'weight': Sum('weight'),
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
        return 'CompostProductionVolume (%d) %s %.2f gallons' % (
            self.pk,
            self.garden,
            self.volume,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(CompostProductionVolume, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs


from .export import (VolumeDataset, WeightDataset, PublicVolumeDataset,
                     PublicWeightDataset)


register('Compost Production by Weight', {
    'add_record_label': 'Add compost by weight',
    'all_gardens_url_name': 'compostproduction_weight_all_gardens',
    'model': CompostProductionWeight,
    'number': 2,
    'garden_detail_url_name': 'compostproduction_weight_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'compostproduction_weight_index',
    'short_name': 'weight',
    'dataset': WeightDataset,
    'public_dataset': PublicWeightDataset,
    'description': _('This report measures the pounds of compost your garden '
                     'produced in a specified time period (top graph) and for '
                     'the whole period you\'ve been collecting this data '
                     '(bottom graph).  Knowing how much compost your garden '
                     'produces measures your garden\'s positive environmental '
                     'impact, and can help you plan for regular soil '
                     'improvements.'),
})


register('Compost Production by Volume', {
    'add_record_label': 'Add compost by volume',
    'all_gardens_url_name': 'compostproduction_volume_all_gardens',
    'model': CompostProductionVolume,
    'number': 2,
    'garden_detail_url_name': 'compostproduction_volume_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'compostproduction_volume_index',
    'short_name': 'volume',
    'dataset': VolumeDataset,
    'public_dataset': PublicVolumeDataset,
    'description': _('This report measures the gallons of compost your garden '
                     'produced in a specified time period (top graph) and for '
                     'the whole period you\'ve been collecting this data '
                     '(bottom graph).  Knowing how much compost your garden '
                     'produces measures your garden\'s positive environmental '
                     'impact, and can help you plan for regular soil '
                     'improvements.'),
})

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


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
        return 'LandfillDiversionWeight (%d) %s %.2f pounds' % (
            self.pk,
            self.garden,
            self.weight,
        )

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
        return 'LandfillDiversionWeight (%d) %s %.2f gallons' % (
            self.pk,
            self.garden,
            self.volume,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LandfillDiversionVolume, cls).get_summarize_kwargs()
        kwargs.update({
            'volume': Sum('volume'),
        })
        return kwargs


from .export import (VolumeDataset, PublicVolumeDataset, WeightDataset,
                     PublicWeightDataset)


register('Landfill Waste Diversion by Weight', {
    'add_record_label': 'Add landfill diversion by weight',
    'all_gardens_url_name': 'landfilldiversion_weight_all_gardens',
    'model': LandfillDiversionWeight,
    'number': 1,
    'garden_detail_url_name': 'landfilldiversion_weight_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'landfilldiversion_weight_index',
    'short_name': 'weight',
    'dataset': WeightDataset,
    'public_dataset': PublicWeightDataset,
    'description': _('This report displays the total pounds of trash your '
                     'garden prevented from going into a landfill by turning '
                     'it into compost instead. Garden composting helps divert '
                     'a significant amount of waste that would have gone into '
                     'the landfill waste stream. Calculating the weight of '
                     'waste diverted measures your garden\'s positive '
                     'environmental impact. The top graph shows waste '
                     'diverted for specified time period, and the bottom '
                     'graph shows the total gallons diverted since you '
                     'started collecting data.'),
})


register('Landfill Waste Diversion by Volume', {
    'add_record_label': 'Add landfill diversion by volume',
    'all_gardens_url_name': 'landfilldiversion_volume_all_gardens',
    'model': LandfillDiversionVolume,
    'number': 1,
    'garden_detail_url_name': 'landfilldiversion_volume_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'landfilldiversion_volume_index',
    'short_name': 'volume',
    'dataset': VolumeDataset,
    'public_dataset': PublicVolumeDataset,
    'description': _('This report displays the total gallons of trash '
                     'prevented from going into a landfill by turning it into '
                     'compost instead. Garden composting helps divert a '
                     'significant amount of waste that would have gone into '
                     'the landfill waste stream. Calculating the volume of '
                     'waste diverted measures your garden\'s positive '
                     'environmental impact. The top graph shows waste '
                     'diverted for specified time period, and the bottom '
                     'graph shows the total gallons diverted since you '
                     'started collecting data.'),
})

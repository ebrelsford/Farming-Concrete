from django.db import models
from django.db.models import Sum

from ..models import BaseMetricRecord
from ..registry import register


class CompostProductionWeight(BaseMetricRecord):
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


class CompostProductionVolume(BaseMetricRecord):
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


register('Compost Production by Weight', {
    'add_record_label': 'Add compost by weight',
    'all_gardens_url_name': 'compostproduction_weight_all_gardens',
    'download_url_name': 'compostproduction_weight_garden_csv',
    'model': CompostProductionWeight,
    'number': 2,
    'garden_detail_url_name': 'compostproduction_weight_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'compostproduction_weight_index',
    'short_name': 'weight',
    'user_gardens_url_name': 'compostproduction_weight_user_gardens',
})


register('Compost Production by Volume', {
    'add_record_label': 'Add compost by volume',
    'all_gardens_url_name': 'compostproduction_volume_all_gardens',
    'download_url_name': 'compostproduction_volume_garden_csv',
    'model': CompostProductionVolume,
    'number': 2,
    'garden_detail_url_name': 'compostproduction_volume_garden_details',
    'group': 'Environmental Data',
    'group_number': 1,
    'index_url_name': 'compostproduction_volume_index',
    'short_name': 'volume',
    'user_gardens_url_name': 'compostproduction_volume_user_gardens',
})

from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class YumYuckQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'crop__name',
            'crop_variety__name',
            'yum_before',
            'yuck_before',
            'yum_after',
            'yuck_after',
        )
        return self.values(*values_args)


class YumYuckManager(MetricManager):
    
    def get_queryset(self):
        return YumYuckQuerySet(self.model)


class YumYuck(BaseMetricRecord):
    objects = YumYuckManager()
    crop = models.ForeignKey('crops.Crop', null=True)
    crop_variety = models.ForeignKey('crops.Variety', blank=True, null=True)

    yum_before = models.PositiveIntegerField(_('yums before'))
    yuck_before = models.PositiveIntegerField(_('yucks before'))
    yum_after = models.PositiveIntegerField(_('yums after'))
    yuck_after = models.PositiveIntegerField(_('yucks after'))

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(YumYuck, cls).get_summarize_kwargs()
        kwargs.update({
            'vegetables': Count('crop'),
            'yum_before': Sum('yum_before'),
            'yuck_before': Sum('yuck_before'),
            'yum_after': Sum('yum_after'),
            'yuck_after': Sum('yuck_after'),
        })
        return kwargs


from .export import YumYuckDataset


register('Changes in Attitude: Yum & Yuck', {
    'add_record_template': 'metrics/yumyuck/change/add_record.html',
    'all_gardens_url_name': 'yumyuck_change_all_gardens',
    'model': YumYuck,
    'number': 1,
    'garden_detail_url_name': 'yumyuck_change_garden_details',
    'group': 'Health Data',
    'group_number': 3,
    'index_url_name': 'yumyuck_change_index',
    'short_name': 'change',
    'dataset': YumYuckDataset,
})

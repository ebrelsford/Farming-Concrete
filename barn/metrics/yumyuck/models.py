from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


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
        record_dicts = self.values(*values_args)

        # Add change in yum
        for record_dict in record_dicts:
            record_dict['change in yums'] = record_dict['yum_after'] - \
                    record_dict['yum_before']
            record_dict['change in yucks'] = record_dict['yuck_after'] - \
                    record_dict['yuck_before']
            for field_to_delete in ('yum_after', 'yum_before', 'yuck_after',
                                    'yuck_before'):
                del record_dict[field_to_delete]

        return record_dicts


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

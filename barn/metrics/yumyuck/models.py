from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class YumYuck(BaseMetricRecord):

    vegetable = models.ForeignKey('farmingconcrete.Variety',
        verbose_name=_('vegetable')
    )

    yum_before = models.PositiveIntegerField(_('yums before'),
        help_text=_('The number of yums before'),
    )

    yuck_before = models.PositiveIntegerField(_('yucks before'),
        help_text=_('The number of yucks before'),
    )

    yum_after = models.PositiveIntegerField(_('yums after'),
        help_text=_('The number of yums after'),
    )

    yuck_after = models.PositiveIntegerField(_('yucks after'),
        help_text=_('The number of yucks after'),
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(YumYuck, cls).get_summarize_kwargs()
        kwargs.update({
            'vegetables': Count('vegetable'),
            'yum_before': Sum('yum_before'),
            'yuck_before': Sum('yuck_before'),
            'yum_after': Sum('yum_after'),
            'yuck_after': Sum('yuck_after'),
        })
        return kwargs


register('Changes in Attitude: Yum & Yuck', {
    'add_record_template': 'metrics/yumyuck/change/add_record.html',
    'all_gardens_url_name': 'yumyuck_change_all_gardens',
    'model': YumYuck,
    'number': 1,
    'garden_detail_url_name': 'yumyuck_change_garden_details',
    'group': 'Health Data',
    'group_number': 3,
    'index_url_name': 'yumyuck_change_index',
    'summarize_template': 'metrics/yumyuck/change/summarize.html',
    'user_gardens_url_name': 'yumyuck_change_user_gardens',
})

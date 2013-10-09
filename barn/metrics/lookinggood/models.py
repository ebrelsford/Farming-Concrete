from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class LookingGoodTag(models.Model):
    event = models.ForeignKey('LookingGoodEvent',
        verbose_name=_('event')
    )


class LookingGoodEvent(BaseMetricRecord):
    start_time = models.TimeField(_('start time'),
        help_text=_('The time that the event started'),
    )

    end_time = models.TimeField(_('end time'),
        help_text=_('The time that the event ended'),
    )

    total_tags = models.PositiveIntegerField(_('total tags'),
        help_text=_('The total number of tags filled out during the event'),
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LookingGoodEvent, cls).get_summarize_kwargs()
        kwargs.update({
            'total_tags': Sum('total_tags'),
        })
        return kwargs


register('Looking Good', {
    'all_gardens_url_name': 'lookinggood_event_all_gardens',
    'model': LookingGoodEvent,
    'garden_detail_url_name': 'lookinggood_event_garden_details',
    'group': 'Health & Wellness',
    'index_url_name': 'lookinggood_event_index',
    'summarize_template': 'metrics/lookinggood/event/summarize.html',
    'user_gardens_url_name': 'lookinggood_event_user_gardens',
})

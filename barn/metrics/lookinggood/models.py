from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class LookingGoodPhoto(models.Model):
    event = models.ForeignKey('LookingGoodEvent',
        verbose_name=_('event')
    )

    photo = models.ImageField(_('photo'),
        upload_to='lookinggood_event',
        blank=True,
        null=True,
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

    comments = models.TextField(_('comments'),
        blank=True,
        null=True,
        help_text=_('Log some tag comments that are particularly striking, '
                    'insightful, or interesting.'),
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LookingGoodEvent, cls).get_summarize_kwargs()
        kwargs.update({
            'total_tags': Sum('total_tags'),
        })
        return kwargs


register('Beauty of the Garden', {
    'add_record_label': 'Add looking good tags',
    'add_record_template': 'metrics/lookinggood/event/add_record.html',
    'all_gardens_url_name': 'lookinggood_event_all_gardens',
    'download_url_name': 'lookinggood_event_garden_csv',
    'model': LookingGoodEvent,
    'number': 4,
    'garden_detail_url_name': 'lookinggood_event_garden_details',
    'group': 'Health Data',
    'group_number': 3,
    'index_url_name': 'lookinggood_event_index',
    'short_name': 'event',
    'user_gardens_url_name': 'lookinggood_event_user_gardens',
})

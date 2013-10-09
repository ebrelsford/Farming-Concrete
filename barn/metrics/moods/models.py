from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class Mood(models.Model):
    name = models.CharField(_('name'),
        max_length=300,
    )

    type = models.CharField(_('type'),
        choices=(
            ('positive', 'positive'),
            ('negative', 'negative'),
            ('neutral', 'neutral'),
        ),
        max_length=50,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class MoodCount(models.Model):
    mood = models.ForeignKey('Mood',
        verbose_name=_('mood'),
    )

    mood_change = models.ForeignKey('MoodChange',
        verbose_name=_('mood change'),
    )

    count = models.PositiveIntegerField(_('count'))

    counted_time = models.CharField(_('counted time'),
        choices=(
            ('in', 'in'),
            ('out', 'out'),
        ),
        max_length=25,
    )

    class Meta:
        ordering = ('counted_time', 'mood__name',)


class MoodChange(BaseMetricRecord):

    recorded_start = models.DateField(_('recorded start'),
        help_text=_('When you started recording mood changes'),
    )

    mood_counts = models.ManyToManyField('Mood',
        through='MoodCount'
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(MoodChange, cls).get_summarize_kwargs()
        kwargs.update({
            # TODO
        })
        return kwargs


register('Good Moods in the Garden', {
    'all_gardens_url_name': 'moods_change_all_gardens',
    'model': MoodChange,
    'garden_detail_url_name': 'moods_change_garden_details',
    'group': 'Health & Wellness',
    'index_url_name': 'moods_change_index',
    'summarize_template': 'metrics/moods/change/summarize.html',
    'user_gardens_url_name': 'moods_change_user_gardens',
})
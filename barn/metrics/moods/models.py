from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class MoodChangeQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'moods',
        )
        return self.annotate(moods=Sum('moodcount__count')) \
                .values(*values_args)


class MoodChangeManager(MetricManager):
    
    def get_queryset(self):
        return MoodChangeQuerySet(self.model)


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
    objects = MoodChangeManager()

    recorded_start = models.DateField(_('recorded start'),
        help_text=_('When you started recording mood changes'),
    )

    mood_counts = models.ManyToManyField('Mood',
        through='MoodCount'
    )

    def __getattr__(self, name):
        # Attempt to get value for mood and time (eg, 'happy_in')
        if name.endswith(('_in', '_out')):
            try:
                name = name.replace('_', ' ')
                mood, time = name.rsplit(' ', 1)
                return self.moodcount_set.get(
                    mood__name=mood,
                    counted_time=time,
                ).count
            except Exception:
                pass
        return super(MoodChange, self).__getattr__(name)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(MoodChange, cls).get_summarize_kwargs()
        kwargs.update({
            # TODO
        })
        return kwargs


from .export import MoodChangeDataset, PublicMoodChangeDataset


register('Good Moods in the Garden', {
    'add_record_template': 'metrics/moods/change/add_record.html',
    'all_gardens_url_name': 'moods_change_all_gardens',
    'model': MoodChange,
    'number': 2,
    'garden_detail_url_name': 'moods_change_garden_details',
    'group': 'Health Data',
    'group_number': 3,
    'index_url_name': 'moods_change_index',
    'short_name': 'change',
    'dataset': MoodChangeDataset,
    'public_dataset': PublicMoodChangeDataset,
})

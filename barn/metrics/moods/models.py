from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class MoodChangeQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'pk',
            'moods',
        )
        record_dicts = self.annotate(moods=Sum('moodcount__count')).values(*values_args)

        # Get positive and negative mood counts for merging
        positive = self.filter(moodcount__mood__type='positive') \
                .annotate(positive_moods=Sum('moodcount__count')) \
                .values('pk', 'positive_moods')
        negative = self.filter(moodcount__mood__type='negative') \
                .annotate(negative_moods=Sum('moodcount__count')) \
                .values('pk', 'negative_moods')

        for record_dict in record_dicts:
            # For the each record, find the positive and negative counts
            for types_dicts in (positive, negative):
                types_dict = filter(lambda x: x['pk'] == record_dict['pk'], types_dicts)[0]
                record_dict.update(types_dict)

            # No longer need the pk
            del record_dict['pk']
        return record_dicts


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

    def __unicode__(self):
        return '%d mood changes' % (self.mood_counts.count(),)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(MoodChange, cls).get_summarize_kwargs()
        kwargs.update({
            # TODO
        })
        return kwargs

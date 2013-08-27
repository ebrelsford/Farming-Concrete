from django.db import models
from django.db.models import Count, Max, Min, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class BaseParticipationMetric(BaseMetricRecord):
    hours = models.DecimalField('hours',
        max_digits=8,
        decimal_places=2,
        help_text=_('Hours of participation in the given date range'),
    )

    recorded_start = models.DateField(_('recorded start'),
        help_text=_('The beginning of the date range for this record'),
    )

    class Meta:
        abstract = True


class HoursByGeography(BaseParticipationMetric):

    # TODO photos

    def __unicode__(self):
        return 'HoursByGeography (%d) %s %.2f hours' % (
            self.pk,
            self.garden,
            self.hours,
        )

    @classmethod
    def summarize(cls, records):
        if not records:
            return None
        return records.aggregate(count=Count('pk'), hours=Sum('hours'),
                                 recorded_min=Min('recorded'),
                                 recorded_max=Max('recorded'))


class Task(models.Model):
    """A type of task that can be worked on and recorded."""
    name = models.CharField(_('name'),
        max_length=200,
    )

    def __unicode__(self):
        return self.name


class HoursByTask(BaseParticipationMetric):
    task = models.ForeignKey('Task',
        verbose_name=_('task'),
        help_text=_('What was being worked on?')
    )
    task_other = models.CharField(_('other task name'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('If you enter "other" for task, enter the task here')
    )

    def __unicode__(self):
        return 'HoursByTask (%d) %s %.2f hours working on %s' % (
            self.pk,
            self.garden,
            self.hours,
            self.task.name,
        )

    @classmethod
    def summarize(cls, records):
        if not records:
            return None
        return records.aggregate(count=Count('pk'), hours=Sum('hours'),
                                 recorded_min=Min('recorded'),
                                 recorded_max=Max('recorded'))


register('Participation Hours by Geography', {
    'model': HoursByGeography,
    'garden_detail_url_name': 'participation_geography_garden_details',
    'group': 'Participation',
    'index_url_name': 'participation_geography_index',
    'summarize_template': 'metrics/participation/geography/summarize.html',
})


#register('Participation Hours by Task', {
    #'model': HoursByTask,
    #'garden_detail_url_name': 'participation_task_garden_details',
    #'group': 'Participation',
    #'index_url_name': 'participation_task_index',
    #'summarize_template': 'metrics/participation/task/summarize.html',
#})

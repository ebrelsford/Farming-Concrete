from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class BaseParticipationMetric(BaseMetricRecord):
    hours = models.DecimalField(_('hours'),
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

    photo = models.ImageField(_('photo'),
        help_text=_('The photo you took to record this'),
        upload_to='participation_geography',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return 'HoursByGeography (%d) %s %.2f hours' % (
            self.pk,
            self.garden,
            self.hours,
        )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(HoursByGeography, cls).get_summarize_kwargs()
        kwargs.update({
            'hours': Sum('hours'),
        })
        return kwargs

    @classmethod
    def summarize(cls, records):
        context = super(HoursByGeography, cls).summarize(records)
        if not context:
            context = {}

        try:
            photo = records.filter(photo__isnull=False).order_by('-added')[0].photo
            context.update({
                'photo': photo,
            })
        except Exception:
            pass
        return context


class Task(models.Model):
    """A type of task that can be worked on and recorded."""
    name = models.CharField(_('name'),
        max_length=200,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class TaskHours(models.Model):
    task = models.ForeignKey('Task',
        verbose_name=_('task'),
    )
    hours_by_task = models.ForeignKey('HoursByTask',
        verbose_name=_('hours by task'),
    )
    hours = models.PositiveIntegerField(_('count'))

    class Meta:
        ordering = ('task__name',)


class HoursByTask(BaseMetricRecord):
    recorded_start = models.DateField(_('recorded start'),
        help_text=_('The beginning of the date range for this record'),
    )
    tasks = models.ManyToManyField('Task',
        through='TaskHours',
        verbose_name=_('tasks'),
    )
    task_other = models.CharField(_('other task name'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('If you enter "other" for task, enter the task here')
    )

    def __getitem__(self, key):
        try:
            return self.taskhours_set.get(task__name=key)
        except Exception:
            return getattr(self, key, None)

    def __unicode__(self):
        return 'HoursByTask (%d) %s' % (self.pk, self.garden,)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(HoursByTask, cls).get_summarize_kwargs()
        #kwargs.update({ }) # TODO
        return kwargs


class Project(models.Model):
    """A project happening at a particular garden."""
    name = models.CharField(_('name'),
        max_length=200,
    )
    garden = models.ForeignKey('farmingconcrete.Garden')

    def __unicode__(self):
        return self.name


class HoursByProject(BaseMetricRecord):
    project = models.ForeignKey('Project',
        help_text=_('The project worked on'),
    )

    gardener = models.ForeignKey('harvestcount.Gardener',
        help_text=_('The gardener who participated in this project'),
    )

    hours = models.DecimalField(_('hours'),
        max_digits=8,
        decimal_places=2,
        help_text=_('Hours of participation on this project'),
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(HoursByProject, cls).get_summarize_kwargs()
        kwargs.update({
            'hours': Sum('hours'),
            'projects': Count('project__pk', distinct=True),
        })
        return kwargs


register('Participation Hours by Geography', {
    'add_record_label': 'Add participation hours',
    'all_gardens_url_name': 'participation_geography_all_gardens',
    'model': HoursByGeography,
    'garden_detail_url_name': 'participation_geography_garden_details',
    'group': 'Participation',
    'index_url_name': 'participation_geography_index',
    'summarize_template': 'metrics/participation/geography/summarize.html',
    'user_gardens_url_name': 'participation_geography_user_gardens',
})


register('Participation Hours by Task', {
    'add_record_label': 'Add participation hours',
    'add_record_template': 'metrics/participation/task/add_record.html',
    'all_gardens_url_name': 'participation_task_all_gardens',
    'model': HoursByTask,
    'garden_detail_url_name': 'participation_task_garden_details',
    'group': 'Participation',
    'index_url_name': 'participation_task_index',
    'summarize_template': 'metrics/participation/task/summarize.html',
    'user_gardens_url_name': 'participation_task_user_gardens',
})


register('Participation Hours by Project', {
    'add_record_label': 'Add participation hours',
    'all_gardens_url_name': 'participation_project_all_gardens',
    'model': HoursByProject,
    'garden_detail_url_name': 'participation_project_garden_details',
    'group': 'Participation',
    'index_url_name': 'participation_project_index',
    'summarize_template': 'metrics/participation/project/summarize.html',
    'user_gardens_url_name': 'participation_project_user_gardens',
})

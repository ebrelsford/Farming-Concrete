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


class HoursByGeography(BaseMetricRecord):

    recorded_start = models.DateField(_('recorded start'),
        help_text=_('The beginning of the date range for this record'),
    )

    neighborhood_definition = models.TextField(blank=True, null=True)

    in_half = models.PositiveIntegerField(
        _('1/2-hour pins "IN"'),
        default=0,
    )
    in_whole = models.PositiveIntegerField(
        _('1-hour pins "IN"'),
        default=0,
    )
    out_half = models.PositiveIntegerField(
        _('1/2-hour pins "OUT"'),
        default=0,
    )
    out_whole = models.PositiveIntegerField(
        _('1-hour pins "OUT"'),
        default=0,
    )

    photo = models.ImageField(_('photo'),
        help_text=_('The photo you took to record this'),
        upload_to='participation_geography',
        blank=True,
        null=True,
    )

    def hours_in(self):
        return self.in_half / 2.0 + self.in_whole
    hours_in = property(hours_in)

    def hours_out(self):
        return self.out_half / 2.0 + self.out_whole
    hours_out = property(hours_out)

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
            'in_half': Sum('in_half'),
            'in_whole': Sum('in_whole'),
            'out_half': Sum('out_half'),
            'out_whole': Sum('out_whole'),
        })
        return kwargs

    @classmethod
    def summarize(cls, records):
        context = super(HoursByGeography, cls).summarize(records)
        if not context:
            context = {}

        context['in'] = context.get('in_half', 0) / 2.0 + context.get('in_whole', 0)
        context['out'] = context.get('out_half', 0) / 2.0 + context.get('out_whole', 0)

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
    task_other = models.CharField(_('What do the other tasks include?'),
        max_length=200,
        blank=True,
        null=True,
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
        kwargs.update({
            'hours': Sum('taskhours__hours'),
        })
        return kwargs


class Project(models.Model):
    """A project happening at a particular garden."""
    name = models.CharField(_('name'),
        max_length=200,
    )
    garden = models.ForeignKey('farmingconcrete.Garden')

    def __unicode__(self):
        return self.name


class ProjectHours(models.Model):
    record = models.ForeignKey('HoursByProject')
    hours = models.PositiveIntegerField(_('hours'))
    gardener = models.ForeignKey('harvestcount.Gardener',
        verbose_name=_('Participant'),
    )


class HoursByProject(BaseMetricRecord):
    project = models.ForeignKey('Project',
        verbose_name=_('project'),
    )

    def __getitem__(self, key):
        try:
            return self.projecthours_set.get(gardener__name=key)
        except Exception:
            return getattr(self, key, None)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(HoursByProject, cls).get_summarize_kwargs()
        kwargs.update({
            'projects': Count('project__pk', distinct=True),
            'participants': Count('projecthours__gardener', distinct=True),
            'hours': Sum('projecthours__hours'),
        })
        return kwargs


register('Participation by Geography', {
    'add_record_label': 'Add participation hours',
    'add_record_template': 'metrics/participation/geography/add_record.html',
    'all_gardens_url_name': 'participation_geography_all_gardens',
    'download_url_name': 'participation_geography_garden_csv',
    'model': HoursByGeography,
    'number': 1,
    'garden_detail_url_name': 'participation_geography_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'participation_geography_index',
    'short_name': 'geography',
    'user_gardens_url_name': 'participation_geography_user_gardens',
})


register('Participation by Task', {
    'add_record_label': 'Add participation hours',
    'add_record_template': 'metrics/participation/task/add_record.html',
    'all_gardens_url_name': 'participation_task_all_gardens',
    'download_url_name': 'participation_task_garden_csv',
    'model': HoursByTask,
    'number': 2,
    'garden_detail_url_name': 'participation_task_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'participation_task_index',
    'short_name': 'task',
    'user_gardens_url_name': 'participation_task_user_gardens',
})


register('Participation by Project', {
    'add_record_label': 'Add participation hours',
    'add_record_template': 'metrics/participation/project/add_record.html',
    'all_gardens_url_name': 'participation_project_all_gardens',
    'download_url_name': 'participation_project_garden_csv',
    'model': HoursByProject,
    'number': 3,
    'garden_detail_url_name': 'participation_project_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'participation_project_index',
    'short_name': 'project',
    'user_gardens_url_name': 'participation_project_user_gardens',
})

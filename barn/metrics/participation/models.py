import re

from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class HoursByGeographyQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'in_half',
            'in_whole',
            'out_half',
            'out_whole',
        )
        record_dicts = self.values(*values_args)

        for record_dict in record_dicts:
            record_dict['hours_in_neighborhood'] = record_dict['in_whole'] + record_dict['in_half'] / 2
            record_dict['hours_outside_neighborhood'] = record_dict['out_whole'] + record_dict['out_half'] / 2
            record_dict['hours'] = record_dict['hours_in_neighborhood'] + \
                    record_dict['hours_outside_neighborhood']

            for pin in ('in_half', 'in_whole', 'out_half', 'out_whole'):
                del record_dict[pin]

        return record_dicts


class HoursByGeographyManager(MetricManager):
    
    def get_queryset(self):
        return HoursByGeographyQuerySet(self.model)


class HoursByTaskQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'pk',
            'hours',
        )
        record_dicts = self.annotate(hours=Sum('taskhours__hours')) \
                .values(*values_args)

        # Rename 'hours'
        for record_dict in record_dicts:
            record_dict['hours worked'] = record_dict['hours']
            del record_dict['hours']

            record = HoursByTask.objects.get(pk=record_dict['pk'])
            for taskhour in record.taskhours_set.all():
                record_dict[taskhour.task.name] = taskhour.hours
            del record_dict['pk']

        return record_dicts


class HoursByTaskManager(MetricManager):
    
    def get_queryset(self):
        return HoursByTaskQuerySet(self.model)


class HoursByProjectQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'hours',
        )
        record_dicts = self.annotate(hours=Sum('projecthours__hours')) \
                .values(*values_args)

        # Rename 'hours'
        for record_dict in record_dicts:
            record_dict['hours spent on project'] = record_dict['hours']
            del record_dict['hours']

        return record_dicts


class HoursByProjectManager(MetricManager):
    
    def get_queryset(self):
        return HoursByProjectQuerySet(self.model)


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
    objects = HoursByGeographyManager()

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
        return '%.2f hours participation by geography' % (
            self.hours_in + self.hours_out,
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
        if not records:
            return None

        context = super(HoursByGeography, cls).summarize(records)
        if not context:
            context = {}

        hours_in = context.get('in_half', 0) / 2.0 + context.get('in_whole', 0)
        hours_out = context.get('out_half', 0) / 2.0 + context.get('out_whole', 0)
        context.update({
            'in': hours_in,
            'out': hours_out,
            'hours': hours_in + hours_out,
        })

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
    objects = HoursByTaskManager()
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

    def __getattr__(self, name):
        # Attempt to get value for task, mostly useful for exporting
        match = re.match(r'task_(\d+)', name)
        if match:
            try:
                task_pk = int(match.group(1))
                return self.taskhours_set.get(task__pk=task_pk).hours
            except Exception:
                pass
        return super(HoursByTask, self).__getattr__(name)

    def __getitem__(self, key):
        try:
            return self.taskhours_set.get(task__name=key)
        except Exception:
            return getattr(self, key, None)

    def __unicode__(self):
        return '%d hours of participation by task' % (
            self.taskhours_set.all().aggregate(hours=Sum('hours'))['hours'],
        )

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
    objects = HoursByProjectManager()
    project = models.ForeignKey('Project',
        verbose_name=_('project'),
    )

    def __getattr__(self, name):
        # Attempt to get value for gardener, mostly useful for exporting
        match = re.match(r'gardener_(\d+)', name)
        if match:
            try:
                gardener_pk = int(match.group(1))
                return self.projecthours_set.get(gardener__pk=gardener_pk).hours
            except Exception:
                return None
        return super(HoursByProject, self).__getattr__(name)

    def __getitem__(self, key):
        try:
            return self.projecthours_set.get(gardener__name=key)
        except Exception:
            return getattr(self, key, None)

    def __unicode__(self):
        return '%d hours of participation by project' % (self.total_hours,)

    def _total_hours(self):
        return self.projecthours_set.aggregate(total_hours=Sum('hours'))['total_hours']
    total_hours = property(_total_hours)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(HoursByProject, cls).get_summarize_kwargs()
        kwargs.update({
            'projects': Count('project__pk', distinct=True),
            'participants': Count('projecthours__gardener', distinct=True),
            'hours': Sum('projecthours__hours'),
        })
        return kwargs

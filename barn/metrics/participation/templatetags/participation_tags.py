import pandas as pd

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options
from classytags.helpers import AsTag
from django import template
from django.db.models import Sum

from metrics.charts import make_chart_name, vertical_bar
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import HoursByGeography, HoursByProject, HoursByTask, Task

register = template.Library()


class HoursByGeographyInChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return HoursByGeography

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('in_half', 'in_whole', 'recorded'),
                                       coerce_float=True)

        df['in_total'] = (df.in_half / 2.0) + df.in_whole
        qdf = df.groupby('recorded').sum()['in_total']
        return vertical_bar(qdf, make_chart_name('participation_geography_in', garden),
                            ylabel='HOURS', shape='short')


class HoursByGeographyOutChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return HoursByGeography

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('out_half', 'out_whole', 'recorded'),
                                       coerce_float=True)

        df['out_total'] = (df.out_half / 2.0) + df.out_whole
        qdf = df.groupby('recorded').sum()['out_total']
        return vertical_bar(qdf, make_chart_name('participation_geography_out', garden),
                            color='#F63C04', ylabel='HOURS', shape='short')


class HoursByGeographyTotal(MetricTotalTag):

    def get_metric_model(self):
        return HoursByGeography

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)

        hours_in = sum([r.hours_in for r in records])
        hours_out = sum([r.hours_out for r in records])
        return hours_in + hours_out


class HoursByProjectChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return HoursByProject

    def get_chart(self, records, garden):
        project_records = []
        for r in records:
            project_records.append({
                'hours': r.projecthours_set.all().aggregate(h=Sum('hours'))['h'],
                'project': r.project,
            })
        df = pd.DataFrame.from_records(project_records, coerce_float=True) \
            .sort(columns='project') \
            .groupby('project') \
            .sum()['hours']
        return vertical_bar(df, make_chart_name('participation_project', garden),
                            ylabel='HOURS')


class HoursByProjectTotal(MetricTotalTag):

    def get_metric_model(self):
        return HoursByProject

    def get_sum_field(self):
        return 'projecthours__hours'


class HoursByTaskChart(ChartMixin, AsTag):
    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('task', required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_metric_model(self):
        return HoursByTask

    def get_value(self, context, garden, start, end, task):
        kwargs = self.args_to_dict(garden, start, end)
        records = self.get_records(**kwargs)
        return self.get_chart(records, kwargs['garden'], task['task'])

    def get_chart(self, records, garden, task):
        task_records = []
        for r in records:
            task_records.append({
                'hours': r[str(task)].hours,
                'recorded': r.recorded,
            })
        df = pd.DataFrame.from_records(task_records)
        qdf = df.groupby('recorded').sum()['hours']
        return vertical_bar(
            qdf,
            make_chart_name('participation_task_%s' % task.replace('/', '_'), garden),
            ylabel='HOURS', shape='short'
        )


class HoursByTaskTotal(MetricTotalTag):

    def get_metric_model(self):
        return HoursByTask

    def get_sum_field(self):
        return 'taskhours__hours'


class GardenerProjectHours(AsTag):
    options = Options(
        Argument('gardener', resolve=True, required=True),
        'for',
        Argument('hours_by_project', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, gardener, hours_by_project):
        return hours_by_project[gardener.name]


class TaskPairs(AsTag):
    options = Options(
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context):
        """Get tasks in pairs, useful for PDF pairing of tasks"""
        tasks = Task.objects.all().values_list('name', flat=True)
        for i in range(0, len(tasks), 2):
            try:
                yield (tasks[i], tasks[i + 1])
            except IndexError:
                yield (tasks[i],)


class TaskHours(AsTag):
    options = Options(
        Argument('task', resolve=True, required=True),
        'for',
        Argument('hours_by_task', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, task, hours_by_task):
        return hours_by_task[task.name]


class GardenPhotos(AsTag):
    options = Options(
        'for',
        Argument('garden', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        return [r.photo for r in HoursByGeography.objects.filter(garden=garden) if r.photo]


register.tag(GardenPhotos)
register.tag(GardenerProjectHours)
register.tag(HoursByGeographyInChart)
register.tag(HoursByGeographyOutChart)
register.tag(HoursByGeographyTotal)
register.tag(HoursByProjectChart)
register.tag(HoursByProjectTotal)
register.tag(HoursByTaskChart)
register.tag(HoursByTaskTotal)
register.tag(TaskHours)
register.tag(TaskPairs)

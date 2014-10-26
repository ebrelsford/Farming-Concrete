import pandas as pd

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template

from metrics.charts import make_chart_name, vertical_bar
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import HoursByGeography

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
register.tag(TaskHours)

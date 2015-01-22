from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from metrics.charts import vertical_bar, line_fill, make_chart_name
from ..models import CompostProductionVolume, CompostProductionWeight

register = template.Library()


class CompostVolumeChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return CompostProductionVolume

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        return vertical_bar(qdf, make_chart_name('compost_volume', garden),
                            ylabel='GALLONS', shape='short')


class CompostVolumeLineChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return CompostProductionVolume

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        return line_fill(qdf.cumsum(),
                         make_chart_name('compost_volume_line', garden),
                         ylabel='GALLONS', shape='short')


class CompostVolumeTotal(MetricTotalTag):

    def get_metric_model(self):
        return CompostProductionVolume

    def get_sum_field(self):
        return 'volume'


class CompostWeightChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return CompostProductionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['weight']
        return vertical_bar(qdf, make_chart_name('compost_weight', garden),
                            ylabel='POUNDS', shape='short')


class CompostWeightLineChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return CompostProductionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['weight']
        return line_fill(qdf.cumsum(),
                         make_chart_name('compost_weight_line', garden),
                         ylabel='POUNDS', shape='short')


class CompostWeightTotal(MetricTotalTag):

    def get_metric_model(self):
        return CompostProductionWeight

    def get_sum_field(self):
        return 'weight'


register.tag(CompostVolumeChart)
register.tag(CompostVolumeLineChart)
register.tag(CompostVolumeTotal)
register.tag(CompostWeightChart)
register.tag(CompostWeightLineChart)
register.tag(CompostWeightTotal)

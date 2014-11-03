from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import line_fill, vertical_bar, make_chart_name
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import LandfillDiversionVolume, LandfillDiversionWeight

register = template.Library()


class LandfilldiversionWeightChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['weight']
        return vertical_bar(qdf, make_chart_name('landfilldiversion_weight', garden),
                            ylabel='LBS', shape='short')


class LandfilldiversionWeightLineChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['weight']
        return line_fill(qdf.cumsum(),
                         make_chart_name('landfilldiversion_weight_line', garden),
                         ylabel='LBS', shape='short')


class LandfilldiversionWeightTotal(MetricTotalTag):

    def get_metric_model(self):
        return LandfillDiversionWeight

    def get_sum_field(self):
        return 'weight'


class LandfilldiversionVolumeChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionVolume

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        return vertical_bar(qdf, make_chart_name('landfilldiversion_volume', garden),
                            ylabel='GALLONS', shape='short')


class LandfilldiversionVolumeLineChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionVolume

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        return line_fill(qdf.cumsum(),
                         make_chart_name('landfilldiversion_volume_line', garden),
                         ylabel='GALLONS', shape='short')


class LandfilldiversionVolumeTotal(MetricTotalTag):

    def get_metric_model(self):
        return LandfillDiversionVolume

    def get_sum_field(self):
        return 'volume'


register.tag(LandfilldiversionWeightChart)
register.tag(LandfilldiversionWeightLineChart)
register.tag(LandfilldiversionWeightTotal)
register.tag(LandfilldiversionVolumeChart)
register.tag(LandfilldiversionVolumeLineChart)
register.tag(LandfilldiversionVolumeTotal)

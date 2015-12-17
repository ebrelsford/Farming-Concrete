from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from metrics.charts import line_fill, vertical_bar, make_chart_name
from units.convert import (preferred_volume_units, preferred_weight_units,
                           to_preferred_volume_units,
                           to_preferred_weight_units)
from ..models import LandfillDiversionVolume, LandfillDiversionWeight

register = template.Library()


class LandfilldiversionWeightChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)
        qdf = df.groupby('recorded').sum()['weight']
        qdf = qdf.apply(lambda x: to_preferred_weight_units(x, garden, force_large_units=True).magnitude)
        units = preferred_weight_units(garden, large=True)
        return vertical_bar(qdf, make_chart_name('landfilldiversion_weight', garden),
                            ylabel=units.upper(), shape='short')


class LandfilldiversionWeightLineChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)
        qdf = df.groupby('recorded').sum()['weight']
        qdf = qdf.apply(lambda x: to_preferred_weight_units(x, garden, force_large_units=True).magnitude)
        units = preferred_weight_units(garden, large=True)
        return line_fill(qdf.cumsum(),
                         make_chart_name('landfilldiversion_weight_line', garden),
                         ylabel=units.upper(), shape='short')


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
        qdf = qdf.apply(lambda x: to_preferred_volume_units(garden,
                                                            cubic_meters=x,
                                                            force_large_units=True).magnitude)
        units = preferred_volume_units(garden, large=True)
        return vertical_bar(qdf, make_chart_name('landfilldiversion_volume', garden),
                            ylabel=units.upper(), shape='short')


class LandfilldiversionVolumeLineChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionVolume

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        qdf = qdf.apply(lambda x: to_preferred_volume_units(garden,
                                                            cubic_meters=x,
                                                            force_large_units=True).magnitude)
        units = preferred_volume_units(garden, large=True)
        return line_fill(qdf.cumsum(),
                         make_chart_name('landfilldiversion_volume_line', garden),
                         ylabel=units.upper(), shape='short')


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

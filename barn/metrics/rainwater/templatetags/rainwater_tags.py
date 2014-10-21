from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import horizontal_bar, line_fill, make_chart_name
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import RainwaterHarvest

register = template.Library()


class RainwaterHarvestChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return RainwaterHarvest

    def get_chart(self, records, garden):
        records = records.filter(volume__isnull=False)
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        return horizontal_bar(qdf, make_chart_name('rainwater', garden),
                              xlabel='GALLONS HARVESTED', shape='short')


class RainwaterHarvestLineChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return RainwaterHarvest

    def get_chart(self, records, garden):
        records = records.filter(volume__isnull=False)
        df = pd.DataFrame.from_records(records.values('volume', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['volume']
        return line_fill(qdf.cumsum(), make_chart_name('rainwater_line', garden),
                         shape='short')


class RainwaterHarvestTotal(MetricTotalTag):

    def get_metric_model(self):
        return RainwaterHarvest

    def get_sum_field(self):
        return 'volume'


register.tag(RainwaterHarvestChart)
register.tag(RainwaterHarvestLineChart)
register.tag(RainwaterHarvestTotal)

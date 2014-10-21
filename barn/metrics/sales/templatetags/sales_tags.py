from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import horizontal_bar, make_chart_name
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import Sale

register = template.Library()


class SalesChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return Sale

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('total_price', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['total_price']
        return horizontal_bar(qdf, make_chart_name('sales', garden),
                              xlabel='TOTAL SOLD')


class SalesTotal(MetricTotalTag):

    def get_metric_model(self):
        return Sale

    def get_sum_field(self):
        return 'total_price'


register.tag(SalesChart)
register.tag(SalesTotal)

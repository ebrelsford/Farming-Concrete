from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from metrics.charts import vertical_bar, make_chart_name
from ..models import Donation

register = template.Library()


class DonationsChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return Donation

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('pounds', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['pounds']
        return vertical_bar(qdf, make_chart_name('donations', garden),
                            ylabel='POUNDS DONATED')


class DonationsTotal(MetricTotalTag):

    def get_metric_model(self):
        return Donation

    def get_sum_field(self):
        return 'pounds'


register.tag(DonationsChart)
register.tag(DonationsTotal)

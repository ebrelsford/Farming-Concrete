from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import horizontal_bar, make_chart_name
from metrics.harvestcount.models import Harvest
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag

register = template.Library()


class HarvestcountChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return Harvest

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('crop__name', 'weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('crop__name').sum()['weight']
        return horizontal_bar(qdf, make_chart_name('harvestcount', garden))


class HarvestcountTotal(MetricTotalTag):

    def get_metric_model(self):
        return Harvest

    def get_sum_field(self):
        return 'weight'


register.tag(HarvestcountChart)
register.tag(HarvestcountTotal)

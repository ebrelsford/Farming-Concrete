from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import horizontal_bar, make_chart_name
from metrics.cropcount.models import Patch
from metrics.templatetags.metrics_tags import ChartMixin

register = template.Library()


class CropcountChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return Patch

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('crop__name', 'quantity', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('crop__name').sum()['quantity']
        return horizontal_bar(qdf, make_chart_name('cropcount', garden),
                              xlabel='NUMBER OF PLANTS')


register.tag(CropcountChart)

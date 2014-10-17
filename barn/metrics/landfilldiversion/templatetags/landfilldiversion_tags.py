from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import vertical_bar, make_chart_name
from metrics.landfilldiversion.models import LandfillDiversionWeight
from metrics.templatetags.metrics_tags import ChartMixin

register = template.Library()


class LandfilldiversionWeightChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LandfillDiversionWeight

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['weight']
        return vertical_bar(qdf, make_chart_name('landfilldiversion_weight', garden),
                            ylabel='POUNDS DIVERTED')


register.tag(LandfilldiversionWeightChart)

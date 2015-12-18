from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from metrics.charts import horizontal_bar, make_chart_name
from metrics.harvestcount.models import Harvest
from units.convert import preferred_weight_units, to_preferred_weight_units

register = template.Library()


class HarvestcountChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return Harvest

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('crop__name', 'weight_new', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('crop__name').sum()['weight_new']
        qdf = qdf.apply(lambda x: to_preferred_weight_units(x, garden, force_large_units=True).magnitude)
        units = preferred_weight_units(garden, large=True)
        return horizontal_bar(qdf, make_chart_name('harvestcount', garden),
                              xlabel=('%s harvested' % units).upper())


class HarvestcountTotal(MetricTotalTag):

    def get_metric_model(self):
        return Harvest

    def get_sum_field(self):
        return 'weight_new'


register.tag(HarvestcountChart)
register.tag(HarvestcountTotal)

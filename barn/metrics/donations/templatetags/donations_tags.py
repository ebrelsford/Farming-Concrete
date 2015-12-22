from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from metrics.charts import vertical_bar, make_chart_name
from units.convert import preferred_weight_units, to_preferred_weight_units
from ..models import Donation

register = template.Library()


class DonationsChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return Donation

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['weight']
        qdf = qdf.apply(lambda x: to_preferred_weight_units(x, garden,
                                                            force_large_units=True).magnitude)
        units = preferred_weight_units(garden, large=True)
        return vertical_bar(qdf, make_chart_name('donations', garden),
                            xlabel=('%s donated by period' % units).upper(),
                            ylabel=units.upper())


class DonationsTotal(MetricTotalTag):

    def get_metric_model(self):
        return Donation

    def get_sum_field(self):
        return 'weight'


register.tag(DonationsChart)
register.tag(DonationsTotal)

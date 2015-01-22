from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from metrics.charts import horizontal_bar, make_chart_name
from ..models import RecipeTally

register = template.Library()


class RecipesChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return RecipeTally

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('recipes_count', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['recipes_count']
        return horizontal_bar(qdf, make_chart_name('recipes', garden),
                              xlabel='TOTAL RECIPES')


class RecipesTotal(MetricTotalTag):

    def get_metric_model(self):
        return RecipeTally

    def get_sum_field(self):
        return 'recipes_count'


register.tag(RecipesChart)
register.tag(RecipesTotal)

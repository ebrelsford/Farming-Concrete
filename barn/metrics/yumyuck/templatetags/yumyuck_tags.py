from django import template
from django.db.models import Count

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import vertical_bar, make_chart_name
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import YumYuck

register = template.Library()


class YumYuckChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return YumYuck

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('crop__name', 'yum_after'),
                                       coerce_float=True)

        qdf = df.groupby('crop__name').sum()['yum_after']
        return vertical_bar(qdf, make_chart_name('yumyuck', garden),
                            ylabel='YUMS AFTER TASTING')


class YumYuckTotal(MetricTotalTag):
    def get_metric_model(self):
        return YumYuck

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        return records.aggregate(crops=Count('crop'))['crops']


register.tag(YumYuckChart)
register.tag(YumYuckTotal)

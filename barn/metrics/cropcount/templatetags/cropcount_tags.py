from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import (ChartMixin,
                                                    MetricRecordsMixin,
                                                    MetricTotalTag)
from metrics.charts import horizontal_bar, make_chart_name
from metrics.cropcount.models import Box, Patch

register = template.Library()


class CropcountChart(ChartMixin, AsTag):

    def get_metric_model(self):
        return Patch

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('crop__name', 'quantity', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('crop__name').sum()['quantity']
        return horizontal_bar(qdf, make_chart_name('cropcount', garden))


class CropcountTotal(MetricTotalTag):

    def get_metric_model(self):
        return Patch

    def get_sum_field(self):
        return 'quantity'


class CropcountTotalBeds(MetricRecordsMixin, AsTag):

    def get_metric_model(self):
        return Patch

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        boxes = Box.objects.filter(patch__in=records).distinct()
        return len(boxes)


class CropcountTotalArea(MetricRecordsMixin, AsTag):

    def get_metric_model(self):
        return Patch

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        boxes = Box.objects.filter(patch__in=records).distinct()
        return sum([b.length * b.width for b in boxes])


register.tag(CropcountChart)
register.tag(CropcountTotal)
register.tag(CropcountTotalBeds)
register.tag(CropcountTotalArea)

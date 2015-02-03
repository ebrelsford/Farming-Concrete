from collections import OrderedDict

from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import (ChartMixin,
                                                    MetricRecordsMixin,
                                                    MetricTotalTag)
from metrics.charts import vertical_bar, make_chart_name
from ..models import LookingGoodEvent, LookingGoodPhoto

register = template.Library()


class GardenPhotos(AsTag):
    options = Options(
        'for',
        Argument('garden', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        return LookingGoodPhoto.objects.filter(event__garden=garden)


class LookingGoodChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return LookingGoodEvent

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values('total_tags', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()['total_tags']
        return vertical_bar(qdf, make_chart_name('lookinggood', garden),
                            shape='short', ylabel='TAGS')


class LookingGoodExampleTags(MetricRecordsMixin, AsTag):

    def get_metric_model(self):
        return LookingGoodEvent

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs).order_by('recorded')
        return OrderedDict([(r.recorded, r.lookinggooditem_set.all()) for r in records])


class LookingGoodTotal(MetricTotalTag):

    def get_metric_model(self):
        return LookingGoodEvent

    def get_sum_field(self):
        return 'total_tags'


register.tag(GardenPhotos)
register.tag(LookingGoodChart)
register.tag(LookingGoodExampleTags)
register.tag(LookingGoodTotal)

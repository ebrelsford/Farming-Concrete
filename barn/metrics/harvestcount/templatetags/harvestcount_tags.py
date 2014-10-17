from datetime import datetime

from django import template

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options
from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import horizontal_bar, make_chart_name
from metrics.harvestcount.models import Harvest
from metrics.templatetags.metrics_tags import MetricRecordTagMixin

register = template.Library()


class HarvestcountChart(MetricRecordTagMixin, AsTag):
    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden, year, start, end):
        # Get KeywordArguments with default values
        kwargs = self.args_to_dict(garden, year, start, end)
        garden = kwargs.get('garden', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        year = kwargs.get('year', datetime.now().year)

        # Get the records requested
        # TODO more generically, offer to other tags
        records = None
        if start and end:
            records = Harvest.get_records(garden, start=start, end=end)
        elif year:
            records = Harvest.get_records(garden, year=year)

        df = pd.DataFrame.from_records(records.values('crop__name', 'weight', 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('crop__name').sum()['weight']
        return horizontal_bar(qdf, make_chart_name('harvestcount', garden),
                              xlabel='POUNDS HARVESTED')


register.tag(HarvestcountChart)

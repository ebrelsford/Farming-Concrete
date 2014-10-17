from datetime import datetime

from django import template
from django.conf import settings

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options
from classytags.helpers import AsTag
import pandas as pd
import pylab

from metrics.cropcount.models import Patch
from metrics.templatetags.metrics_tags import MetricRecordTagMixin

register = template.Library()


class CropcountChart(MetricRecordTagMixin, AsTag):

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
        year = kwargs.get('year', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        year = kwargs.get('year', datetime.now().year)

        # Get the records requested
        # TODO more generically, offer to other tags
        records = None
        if start and end:
            records = Patch.get_records(garden, start=start, end=end)
        elif year:
            records = Patch.get_records(garden, year=year)

        df = pd.DataFrame.from_records(records.values('crop__name', 'quantity',
                                                      'recorded'),
                                       coerce_float=True)
        qdf = df.groupby('recorded').sum()['quantity']
        qdf.plot(kind='bar')

        # TODO set destination to more explicit folder, make this a method
        #  /generated_charts/cropcount/garden_date_count.png
        pylab.savefig(settings.MEDIA_ROOT + '/test' + '/blah.png', bbox_inches='tight')
        return 'test/blah.png'


register.tag(CropcountChart)

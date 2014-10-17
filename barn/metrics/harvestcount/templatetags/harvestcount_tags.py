from datetime import datetime

from django import template
from django.conf import settings

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options
from classytags.helpers import AsTag
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pandas as pd
import pylab

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
        year = kwargs.get('year', None)
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
        qdf.plot(kind='barh', color='#849F38', linewidth=0)

        ax = plt.gca()
        ax.yaxis.grid(False)

        ax.set_ylabel('')
        ax.set_xlabel('POUNDS HARVESTED', fontsize=12, fontweight='bold')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(direction='out')
        ax.yaxis.set_ticks_position('left')
        ax.yaxis.set_tick_params(direction='out', labelsize=14)

        # Add labels to rectangles
        for rect in ax.get_children():
            if not isinstance(rect, Rectangle):
                continue
            if rect.get_facecolor() == (1, 1, 1, 1):
                continue
            width = rect.get_width()
            ax.text(width - (qdf.max() * 0.05),
                    rect.get_y() + rect.get_height() / 2. - .03,
                    '%d' % int(width), ha='center', va='bottom', color='white',
                    fontweight='bold')

        # TODO set destination to more explicit folder, make this a method
        #  /generated_charts/cropcount/garden_date_count.png
        pylab.savefig(settings.MEDIA_ROOT + '/test' + '/blah2.png', bbox_inches='tight')
        plt.clf()
        plt.cla()
        return 'test/blah2.png'


register.tag(HarvestcountChart)

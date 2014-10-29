from django import template
from django.db.models import Count, Sum

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import vertical_bar, make_chart_name
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import MoodChange, MoodCount

register = template.Library()


class MoodsMixin(object):

    def find_moods_difference(self, records, mood_type):
        """
        Find the difference in recorded moods on entering or leaving the 
        garden.
        """
        moodcounts = MoodCount.objects.filter(
            mood_change__in=records,
            mood__type=mood_type,
        )
        chart_counts = []
        for mood in list(set(moodcounts.values_list('mood__name', flat=True))):
            mood_in = moodcounts.filter(counted_time='in', mood__name=mood) \
                    .aggregate(s=Sum('count'))['s']
            mood_out = moodcounts.filter(counted_time='out', mood__name=mood) \
                    .aggregate(s=Sum('count'))['s']
            chart_counts.append({
                'mood': mood,
                'change': mood_out - mood_in,
            })
        return chart_counts


class MoodsPositiveChart(MoodsMixin, ChartMixin, AsTag):
    def get_metric_model(self):
        return MoodChange

    def get_chart(self, records, garden):
        chart_counts = self.find_moods_difference(records, 'positive')
        df = pd.DataFrame.from_records(chart_counts, coerce_float=True)
        return vertical_bar(df.groupby('mood').sum()['change'],
                            make_chart_name('moods_positive', garden),
                            ylabel='CHANGE IN POSITIVE MOODS', shape='short')


class MoodsNegativeChart(MoodsMixin, ChartMixin, AsTag):
    def get_metric_model(self):
        return MoodChange

    def get_chart(self, records, garden):
        chart_counts = self.find_moods_difference(records, 'negative')
        df = pd.DataFrame.from_records(chart_counts, coerce_float=True)
        return vertical_bar(df.groupby('mood').sum()['change'],
                            make_chart_name('moods_negative', garden),
                            ylabel='CHANGE IN NEGATIVE MOODS', shape='short')


class MoodsTotal(MetricTotalTag):
    def get_metric_model(self):
        return MoodChange

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        return records.aggregate(total=Count('pk'))['total']


register.tag(MoodsPositiveChart)
register.tag(MoodsNegativeChart)
register.tag(MoodsTotal)

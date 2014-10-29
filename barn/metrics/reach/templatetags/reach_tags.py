from django import template

from classytags.helpers import AsTag
import pandas as pd

from metrics.charts import vertical_bar, make_chart_name
from metrics.templatetags.metrics_tags import ChartMixin, MetricTotalTag
from ..models import ProgramReach

register = template.Library()

age_fields = ('age_10', 'age_10_14', 'age_15_19', 'age_20_24', 'age_25_34',
              'age_35_44', 'age_45_54', 'age_55_64', 'age_65',)


class ReachAgeChart(ChartMixin, AsTag):
    def get_metric_model(self):
        return ProgramReach

    def get_chart(self, records, garden):
        df = pd.DataFrame.from_records(records.values(*age_fields), coerce_float=True)
        columns = dict([(a, a.replace('age_', '').replace('_', '-')) for a in age_fields])
        columns['age_10'] = 'under 10'
        columns['age_65'] = '65+'
        df = df.rename(columns=columns).sum().transpose()
        return vertical_bar(df, make_chart_name('reach_age', garden),
                            ylabel='PARTICIPANTS')


class ReachTotal(MetricTotalTag):
    def get_metric_model(self):
        return ProgramReach

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        total_participants = 0
        for record in records:
            total_participants += sum([getattr(record, f) or 0 for f in age_fields])
        return total_participants


register.tag(ReachAgeChart)
register.tag(ReachTotal)

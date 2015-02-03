from collections import OrderedDict

from django import template
from django.db.models import Sum

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options
from classytags.helpers import AsTag
import pandas as pd

from metrics.base.templatetags.metrics_tags import (ChartMixin,
                                                    MetricRecordsMixin,
                                                    MetricTotalTag)
from metrics.charts import vertical_bar, make_chart_name
from ..models import SmartsAndSkills

register = template.Library()


class SkillsChart(ChartMixin, AsTag):
    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('shared', required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_metric_model(self):
        return SmartsAndSkills

    def get_value(self, context, garden, start, end, shared):
        shared = shared['shared']
        kwargs = self.args_to_dict(garden, start, end)
        records = self.get_records(**kwargs)
        return self.get_chart(records, kwargs['garden'], shared)

    def get_chart(self, records, garden, shared):
        df = pd.DataFrame.from_records(records.values(shared, 'recorded'),
                                       coerce_float=True)

        qdf = df.groupby('recorded').sum()[shared]
        return vertical_bar(qdf, make_chart_name('skills_%s' % shared, garden),
                            shape='short',
                            ylabel='NUMBER OF %s' % shared.upper().replace('_', ' '))


class SkillsExamples(MetricRecordsMixin, AsTag):
    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('shared', required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_metric_model(self):
        return SmartsAndSkills

    def get_value(self, context, garden, start, end, shared):
        shared = shared['shared']
        kwargs = self.args_to_dict(garden, start, end)
        records = self.get_records(**kwargs).order_by('recorded')
        return OrderedDict([(r.recorded, getattr(r, '%s_examples' % shared)) 
                            for r in records])


class SkillsTotal(MetricTotalTag):
    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('shared', required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_metric_model(self):
        return SmartsAndSkills

    def get_value(self, context, garden, start, end, shared):
        shared = shared['shared']
        kwargs = self.args_to_dict(garden, start, end)
        records = self.get_records(**kwargs)
        return records.aggregate(total=Sum(shared))['total']


class SkillsShareds(AsTag):
    options = Options(
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context):
        shared = (
            'skills_shared',
            'concepts_shared',
            'projects_proposed',
            'ideas_to_learn',
            'intentions_to_collaborate',
        )
        return dict([(s, s.replace('_', ' ')) for s in shared])


register.tag(SkillsChart)
register.tag(SkillsExamples)
register.tag(SkillsShareds)
register.tag(SkillsTotal)

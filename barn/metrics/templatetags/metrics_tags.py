from itertools import groupby
from operator import itemgetter

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options, Tag
from classytags.helpers import AsTag, InclusionTag

from ..registry import registry

register = template.Library()


# TODO list_records (dynamically get template name)


class MetricRecordTagMixin(object):

    def args_to_dict(self, *args):
        """
        Gather KeywordArguments into a dict
        """
        kwargs = {}
        for arg in args:
            for k, v in arg.items():
                kwargs[k] = v
        return kwargs

    def sort_metrics(self, metrics):
        return sorted(metrics, key=itemgetter('group', 'name'))

    def group_metrics(self, metrics):
        grouped = groupby(metrics, lambda m: m['group'])
        g = {}
        for group, metric_list in grouped:
            g[group] = list(metrics)
        return g

    def count_recorded_metrics(self, metric_model, garden, start=None,
                               end=None, year=None):
        if start and end:
            count = metric_model.get_records(garden, start=start, end=end).count()
        elif year:
            count = metric_model.get_records(garden, year=year).count()
        else:
            count = metric_model.get_records(garden).count()
        return count


class CountRecords(MetricRecordTagMixin, AsTag):

    options = Options(
        Argument('name'),
        KeywordArgument('garden', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, name, garden, year, start, end):
        # Get KeywordArguments with default values
        kwargs = self.args_to_dict(garden, year, start, end)
        garden = kwargs.get('garden', None)
        year = kwargs.get('year', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        if not year:
            year = settings.FARMINGCONCRETE_YEAR

        # Get the records requested
        metric = registry[name]['model']
        if start and end:
            return metric.get_records(garden, start=start, end=end).count()
        elif year:
            return metric.get_records(garden, year=year).count()
        return 0


class Summarize(MetricRecordTagMixin, Tag):

    options = Options(
        Argument('name'),
        KeywordArgument('summary', required=False),
        KeywordArgument('records', required=False),
        KeywordArgument('garden', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
    )

    def render_tag(self, context, name, summary, records, garden, year, start,
                   end):
        kwargs = self.args_to_dict(summary, records, garden, year, start, end)

        # Get KeywordArguments with default values
        summary = kwargs.get('summary', None)
        records = kwargs.get('records', None)
        garden = kwargs.get('garden', None)
        year = kwargs.get('year', settings.FARMINGCONCRETE_YEAR)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)

        # Get the summary requested
        metric = registry[name]['model']
        if records and not summary:
            # If we do not have a summary, calculate it
            summary = metric.summarize(records)
        if not summary:
            # If we do not have records either, get them and summarize
            if start and end:
                summary = metric.get_summary_data(garden, start=start, end=end)
            else:
                summary = metric.get_summary_data(garden, year=year)

        if not summary:
            return ''
        return render_to_string(self.get_template(name), summary)

    def get_template(self, metric_name):
        try:
            template_name = registry[metric_name]['summarize_template']
        except Exception:
            app_label = registry[metric_name]['model']._meta.app_label
            template_name = 'metrics/%s/summarize.html' % app_label
        return template_name


class MetricsWithRecords(MetricRecordTagMixin, AsTag):

    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('grouped', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden, year, start, end, grouped):
        # Get KeywordArguments with default values
        kwargs = self.args_to_dict(garden, year, start, end)
        garden = kwargs.get('garden', None)
        year = kwargs.get('year', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        grouped = kwargs.get('grouped', False)
        if not year:
            year = settings.FARMINGCONCRETE_YEAR

        metrics_with_records = []
        for metric in registry.values():
            model = metric['model']
            count = self.count_recorded_metrics(model, garden, start=start,
                                                end=end, year=year)
            if count:
                metrics_with_records.append(metric)

        sorted_metrics = self.sort_metrics(metrics_with_records)
        if grouped:
            return self.group_metrics(sorted_metrics)
        return sorted_metrics


class MetricsWithoutRecords(MetricRecordTagMixin, AsTag):

    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('grouped', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden, year, start, end, grouped):
        # Get KeywordArguments with default values
        kwargs = self.args_to_dict(garden, year, start, end)
        garden = kwargs.get('garden', None)
        year = kwargs.get('year', None)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        grouped = kwargs.get('grouped', False)
        if not year:
            year = settings.FARMINGCONCRETE_YEAR

        metrics_without_records = []
        for metric in registry.values():
            model = metric['model']
            count = self.count_recorded_metrics(model, garden, start=start,
                                                end=end, year=year)
            if not count:
                metrics_without_records.append(metric)

        sorted_metrics = self.sort_metrics(metrics_without_records)
        if grouped:
            return self.group_metrics(sorted_metrics)
        return sorted_metrics


class AddRecord(MetricRecordTagMixin, InclusionTag):

    options = Options(
        Argument('metric_name'),
        Argument('garden'),
        Argument('form'),
    )

    template = ''

    def get_context(self, context, metric_name, garden, form):
        context.update({
            'add_record_label': registry[metric_name].get('add_record_label'),
            'form': form,
        })
        return context

    def get_template(self, context, metric_name, garden, form):
        try:
            template_name = registry[metric_name]['add_record_template']
        except Exception:
            template_name = 'metrics/add_record.html'
        return template_name


class MetricContentType(AsTag):

    options = Options(
        Argument('metric', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, metric):
        return ContentType.objects.get_for_model(metric['model'])


class IfCanDelete(Tag):
    name = 'ifcandelete'
    options = Options(
        Argument('metric'),
        blocks=[('endifcandelete', 'nodelist')],
    )

    def render_tag(self, context, metric, nodelist):
        user = context['user']
        meta = metric['model']._meta
        if user.has_perm('%s.%s' % (meta.app_label, meta.get_delete_permission(),)):
            return nodelist.render(context)
        return ''


register.tag(AddRecord)
register.tag(CountRecords)
register.tag(IfCanDelete)
register.tag(Summarize)
register.tag(MetricContentType)
register.tag(MetricsWithRecords)
register.tag(MetricsWithoutRecords)

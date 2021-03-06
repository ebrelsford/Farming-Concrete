from datetime import datetime
import itertools
from itertools import groupby
import logging
from operator import itemgetter

from django import template
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max, Sum
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string, select_template

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options, Tag
from classytags.helpers import AsTag, InclusionTag

from ...registry import registry
from ...utils import get_min_recorded

logger = logging.getLogger(__name__)
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
        return sorted(metrics, key=itemgetter('group_number', 'number'))

    def group_metrics(self, metrics):
        grouped = groupby(metrics, lambda m: m['group'])
        g = {}
        for group, metric_list in grouped:
            g[group] = list(metric_list)
        return g

    def count_recorded_metrics(self, metric_model, garden, start=None,
                               end=None, year=None):
        if start and end:
            count = metric_model.get_records(gardens=garden, start=start, end=end).count()
        elif year:
            count = metric_model.get_records(gardens=garden, year=year).count()
        else:
            count = metric_model.get_records(gardens=garden).count()
        return count

    def get_template_candidates(self, metric_name, filename):
        return [d + filename for d in self.get_template_dirs(metric_name)]

    def get_template_dirs(self, metric_name):
        app_label = registry[metric_name]['model']._meta.app_label
        model_name = registry[metric_name]['model']._meta.model_name
        short_name = registry[metric_name].get('short_name', model_name)
        return [
            'metrics/%s/%s/' % (app_label, short_name),
            'metrics/%s/%s/' % (app_label, model_name),
            'metrics/%s/' % app_label,
        ]


class MetricRecordsMixin(MetricRecordTagMixin):
    options = Options(
        KeywordArgument('garden', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_metric_model(self):
        raise NotImplementedError('Implement MetricRecordsMixin.get_metric_model()')

    def get_records(self, garden=None, start=None, end=None, year=None):
        metric_model = self.get_metric_model()
        if start and end:
            return metric_model.get_records(gardens=garden, start=start, end=end)
        elif year:
            return metric_model.get_records(gardens=garden, year=year)


class ChartMixin(MetricRecordsMixin):

    def get_chart(self, records, garden):
        raise NotImplementedError('Implement ChartMixin.get_chart()')

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        try:
            return self.get_chart(records, kwargs['garden'])
        except Exception:
            logger.exception('Exception while generating report chart')
            return None


class MetricTotalTag(MetricRecordsMixin, AsTag):

    def get_sum_field(self):
        raise NotImplementedError('Implement MetricTotalTag.get_sum_field()')

    def get_value(self, context, garden, year, start, end):
        kwargs = self.args_to_dict(garden, year, start, end)
        records = self.get_records(**kwargs)
        return records.aggregate(total=Sum(self.get_sum_field()))['total']


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
        year = kwargs.get('year', datetime.now().year)

        # Get the records requested
        metric = registry[name]['model']
        if start and end:
            return metric.get_records(gardens=garden, start=start, end=end).count()
        elif year:
            return metric.get_records(gardens=garden, year=year).count()
        return 0


class Summarize(MetricRecordTagMixin, Tag):

    empty_template_name = 'metrics/summarize_empty.html'

    options = Options(
        Argument('name'),
        KeywordArgument('summary', required=False),
        KeywordArgument('records', required=False),
        KeywordArgument('garden', required=False),
        KeywordArgument('gardens', required=False),
        KeywordArgument('year', required=False),
        KeywordArgument('start', required=False),
        KeywordArgument('end', required=False),
        KeywordArgument('page', required=False),
    )

    def render_tag(self, context, name, summary, records, garden, gardens,
                   year, start, end, page):
        kwargs = self.args_to_dict(summary, records, garden, gardens, year,
                                   start, end, page)

        # Get KeywordArguments with default values
        summary = kwargs.get('summary', None)
        records = kwargs.get('records', None)
        garden = kwargs.get('garden', None)
        gardens = kwargs.get('gardens', None)
        year = kwargs.get('year', datetime.now().year)
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        page = kwargs.get('page', 'list')

        # Get the summary requested
        metric = registry[name]['model']
        if records and not summary:
            # If we do not have a summary, calculate it
            summary = metric.summarize(records)
        if not summary:
            # If we do not have records either, get them and summarize
            if start and end:
                summary = metric.get_summary_data(gardens, start=start, end=end)
            else:
                summary = metric.get_summary_data(gardens, year=year)

        if not summary:
            if page == 'detail':
                return ''
            return render_to_string(self.empty_template_name)

        if gardens:
            summary['gardens'] = gardens
        else:
            summary['gardens'] = (garden,)
        templates = self.get_page_templates(name, page) + self.get_templates(name)
        for template in templates:
            try:
                return render_to_string(template, summary)
            except TemplateDoesNotExist:
                continue

    def get_page_templates(self, metric_name, page):
        if page == 'detail':
            return self.get_template_candidates(metric_name, 'summarize_detail.html')
        return []

    def get_templates(self, metric_name):
        templates = self.get_template_candidates(metric_name, 'summarize.html')
        try:
            templates = [registry[metric_name]['summarize_template']] + templates
        except Exception:
            pass
        return templates


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
        year = kwargs.get('year', datetime.now().year)

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
        year = kwargs.get('year', datetime.now().year)

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
        templates = self.get_template_candidates(metric_name, 'add_record.html')
        templates = templates + ['metrics/add_record.html',]
        try:
            templates = [registry[metric_name]['add_record_template'],] + templates
        except Exception:
            pass
        return select_template(templates).template.name


class MetricContentType(AsTag):

    options = Options(
        Argument('metric', resolve=True, required=True),
        'for',
        Argument('model', resolve=True, required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, metric, model):
        if model:
            app_name, model_name = model.split('.')
            return ContentType.objects.get_by_natural_key(app_name, model_name)
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
        if user.has_perm('%s.%s' % (meta.app_label, get_permission_codename('delete', meta))):
            return nodelist.render(context)
        return ''


class MetricYears(MetricRecordTagMixin, AsTag):
    """
    Get years for which we have data for the given garden and metric.
    """

    options = Options(
        Argument('metric'),
        Argument('garden'),
        'as',
        Argument('varname', resolve=False),
    )

    def get_value(self, context, metric, garden):
        records = metric['model'].objects.for_garden(garden)
        recordeds = list(records.values_list('recorded', flat=True).order_by('recorded'))
        min_year = datetime.now().year - 1
        try:
           min_year = min(min_year, recordeds[0].year)
        except Exception:
            pass
        max_year = datetime.now().year
        try:
           max_year = max(max_year, recordeds[-1].year)
        except Exception:
            pass
        return [year for year in range(min_year, max_year + 1)]


class GardenYearsRecorded(AsTag):
    """Get each year that a given garden has some records of any type."""
    options = Options(
        Argument('garden'),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        metric_models = [m['model'] for m in registry.values()]
        years = [m.objects.for_garden(garden).dates('recorded', 'year') for m in
                 metric_models]
        years = [list(y) for y in years if y]
        years = [y.year for y in list(set(itertools.chain.from_iterable(years)))]
        return sorted(years)


class GardenMaxRecorded(MetricRecordTagMixin, AsTag):
    """Get the date of the latest record of any type for a given garden."""
    options = Options(
        Argument('garden'),
        KeywordArgument('metric', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden, metric):
        kwargs = self.args_to_dict(metric)
        metric = kwargs.get('metric', None)
        if not metric:
            metric_models = [m['model'] for m in registry.values()]
        else:
            metric_models = [registry[metric]['model'],]
        max_dates = [m.objects.for_garden(garden).aggregate(max_date=Max('recorded'))['max_date'] for
                     m in metric_models]
        try:
            return max(filter(None, max_dates))
        except ValueError:
            return None


class GardenMinRecorded(AsTag):
    """Get the date of the earliest record of any type for a given garden."""
    options = Options(
        Argument('garden'),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        return get_min_recorded(garden)


class MetricReportPage(MetricRecordTagMixin, InclusionTag):
    options = Options(
        Argument('metric_name'),
        Argument('garden'),
    )

    template = ''

    def get_context(self, context, metric_name, garden):
        return context

    def get_template(self, context, metric_name, garden):
        templates = self.get_template_candidates(metric_name, 'report_page.html')
        templates = templates + ['metrics/report_page.html',]
        try:
            templates = [registry[metric_name]['report_page_template'],] + templates
        except Exception:
            pass
        return select_template(templates).template.name


register.tag(AddRecord)
register.tag(CountRecords)
register.tag(GardenMaxRecorded)
register.tag(GardenMinRecorded)
register.tag(GardenYearsRecorded)
register.tag(IfCanDelete)
register.tag(Summarize)
register.tag(MetricContentType)
register.tag(MetricReportPage)
register.tag(MetricYears)
register.tag(MetricsWithRecords)
register.tag(MetricsWithoutRecords)

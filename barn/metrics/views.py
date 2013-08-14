from django.views.generic import DetailView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.dates import YearMixin

from farmingconcrete.models import Garden
from generic.views import LoginRequiredMixin


class MetricMixin(ContextMixin):
    """
    A mixin that provides metric-specific context.
    """

    def get_index_url(self):
        raise NotImplemented('Implement get_index_url')

    def get_metric_name(self):
        raise NotImplemented('Implement get_metric_name')

    def get_context_data(self, **kwargs):
        context = super(MetricMixin, self).get_context_data(**kwargs)
        context.update({
            'index_url': self.get_index_url(),
            'metric_name': self.get_metric_name(),
        })
        return context


class DefaultYearMixin(YearMixin):

    def get_default_year(self):
        raise NotImplemented('Implement get_default_year')

    def get_year(self):
        try:
            year = super(DefaultYearMixin, self).get_year()
        except Exception:
            year = None
        return year or self.get_default_year()


class RecordsMixin(DefaultYearMixin):
    """
    A mixin that aids in retrieving records (instances of models that derive
    from BaseMetricRecord) for a particular year.
    """

    def get_records(self):
        return self.metric_model.objects.filter(recorded__year=self.get_year())


class IndexView(LoginRequiredMixin, RecordsMixin, TemplateView):
    """
    The index / landing page for a metric.
    """

    def get_template_names(self):
        return [
            '%s/index.html' % self.metric_model._meta.app_label,
        ]


class UserGardenView(TemplateView):
    pass


class AllGardensView(TemplateView):
    pass


class GardenView(LoginRequiredMixin, RecordsMixin, DetailView):
    model = Garden

    def get_records(self):
        return super(GardenView, self).get_records().filter(garden=self.object)

    def get_template_names(self):
        return [
            '%s/gardens/detail.html' % self.metric_model._meta.app_label,
        ]


class SummaryView(TemplateView):
    pass


class AddView():
    pass


class DeleteView():
    pass

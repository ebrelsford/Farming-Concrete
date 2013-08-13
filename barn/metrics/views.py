from django.views.generic import DetailView, TemplateView
from django.views.generic.dates import YearMixin

from generic.views import LoginRequiredMixin


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
        return self.model.objects.filter(added__year=self.get_year())


class IndexView(LoginRequiredMixin, RecordsMixin, TemplateView):
    """
    The index / landing page for a metric.
    """

    def get_template_names(self):
        return [
            '%s/index.html' % self.model._meta.app_label,
        ]


class UserGardenView(TemplateView):
    pass


class AllGardensView(TemplateView):
    pass


class GardenView(DetailView):
    pass


class SummaryView(TemplateView):
    pass


class AddView():
    pass


class DeleteView():
    pass

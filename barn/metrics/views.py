from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.dates import YearMixin

from farmingconcrete.models import Garden
from generic.views import LoginRequiredMixin


class MetricMixin(ContextMixin):
    """
    A mixin that provides metric-specific context.
    """

    def get_index_url(self):
        raise NotImplementedError('Implement get_index_url')

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
        raise NotImplementedError('Implement get_default_year')

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


class UserGardenView(LoginRequiredMixin, ListView):

    def get_template_names(self):
        return [
            '%s/gardens/user_gardens.html' % self.metric_model._meta.app_label,
        ]

    def get_queryset(self):
        type = self.request.session['garden_type']

        profile = self.request.user.get_profile()
        user_gardens = profile.gardens.all()
        if type != 'all':
            user_gardens = user_gardens.filter(type=type)
        return user_gardens

    def get_context_data(self, **kwargs):
        user_gardens = self.get_queryset()

        context = super(UserGardenView, self).get_context_data(**kwargs)
        context.update({
            'user_gardens': user_gardens.order_by('name'),
            'user_garden_ids': user_gardens.values_list('id', flat=True),
        })
        return context


class AllGardensView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        return [
            '%s/gardens/all_gardens.html' % self.metric_model._meta.app_label,
        ]

    def get_all_gardens_with_records(self):
        raise NotImplementedError('Implement get_all_gardens_with_records')

    def get_user_gardens(self):
        profile = self.request.user.get_profile()
        user_gardens = profile.gardens.all()

        type = self.request.session['garden_type']
        if type and type != 'all':
            user_gardens = user_gardens.filter(type=type)
        return user_gardens

    def get_context_data(self, **kwargs):
        context = super(AllGardensView, self).get_context_data(**kwargs)
        context.update({
            'all_gardens_with_records': self.get_all_gardens_with_records(),
            'user_gardens': self.get_user_gardens(),
        })
        return context


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
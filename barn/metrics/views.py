from datetime import date, datetime

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Manager
from django.http import HttpResponse
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from accounts.utils import get_profile
from farmingconcrete.models import Garden
from farmingconcrete.views import FarmingConcreteYearMixin
from generic.views import (CSVView, LoginRequiredMixin,
                           PermissionRequiredMixin, SuccessMessageFormMixin)

from .registry import registry


class MetricMixin(ContextMixin):
    """
    A mixin that provides metric-specific context.
    """

    def get_index_url(self):
        try:
            return reverse(registry[self.get_metric_name()]['index_url_name'])
        except:
            return None

    def get_metric_name(self):
        raise NotImplemented('Implement get_metric_name')

    def get_metric(self):
        return registry[self.get_metric_name()]

    def get_metric_model(self):
        return registry[self.get_metric_name()]['model']

    def set_year(self):
        year = self.kwargs.get('year', None)
        if year:
            self.request.session['year'] = year

    def get_context_data(self, **kwargs):
        self.set_year()
        context = super(MetricMixin, self).get_context_data(**kwargs)
        context.update({
            'index_url': self.get_index_url(),
            'metric_name': self.get_metric_name(),
            'metric': self.get_metric(),
            'page_type': 'data_entry',
        })
        return context


class RecordsMixin(FarmingConcreteYearMixin):
    """
    A mixin that aids in retrieving records (instances of models that derive
    from BaseMetricRecord) for a particular year.
    """

    def get_records(self):
        return self.metric_model.objects.for_year(self.get_year())


class RecordedGardensMixin(object):

    def filter_gardens_by_type(self, qs):
        type = self.request.session.get('garden_type', 'all')
        if type and type != 'all':
            qs = qs.filter(type=type)
        return qs


class DeleteRecordView(DeleteView):

    def get_queryset(self):
        record_type_pk = self.kwargs.get('record_type_pk', None)
        record_model = ContentType.objects.get_for_id(record_type_pk).model_class()
        return record_model._default_manager.all()

    def can_delete(self, user, record):
        if user.is_superuser:
            return True
        if (self.not_too_old(record) and self.has_permission(user, record) and
            self.can_edit_garden(user, record)):
            return True
        return False

    def not_too_old(self, record):
        now = datetime.now()
        a_year_ago = now.replace(year=now.year - 1)
        return record.added > a_year_ago

    def can_edit_garden(self, user, record):
        if user.has_perm('farmingconcrete.can_edit_any_garden'):
            return True
        return get_profile(user).gardens.filter(pk=record.garden.pk).count() > 0

    def has_permission(self, user, record):
        meta = self.object._meta
        perm = '%s.%s' % (meta.app_label, meta.get_delete_permission(),)
        return user.has_perm(perm)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.can_delete(self.request.user, self.object):
            raise PermissionDenied
        self.object.delete()
        return HttpResponse('OK')


class IndexView(LoginRequiredMixin, RecordsMixin, TemplateView):
    """
    The index / landing page for a metric.
    """

    def get_user_gardens(self):
        type = self.request.session.get('garden_type', 'all')
        profile = get_profile(self.request.user)
        user_gardens = profile.gardens.all()
        if type != 'all':
            user_gardens = user_gardens.filter(type=type)
        return user_gardens

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        records = self.get_records()
        context.update({
            'summary': self.metric_model.summarize(records),
            'user_gardens': self.get_user_gardens().order_by('name'),
        })
        return context

    def get_template_names(self):
        templates = [
            'metrics/%s/index.html' % self.metric_model._meta.app_label,
        ]
        if self.template_name:
            templates = [self.template_name] + templates
        return templates


class UserGardenView(LoginRequiredMixin, ListView):

    def get_template_names(self):
        return [
            'metrics/%s/gardens/user_gardens.html' % self.metric_model._meta.app_label,
            'metrics/user_gardens.html',
        ]

    def get_queryset(self):
        type = self.request.session.get('garden_type', 'all')

        profile = get_profile(self.request.user)
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


class AllGardensView(RecordedGardensMixin, LoginRequiredMixin,
                     PermissionRequiredMixin, TemplateView):
    permission = 'farmingconcrete.can_edit_any_garden'

    def get_template_names(self):
        return [
            'metrics/%s/gardens/all_gardens.html' % self.metric_model._meta.app_label,
            'metrics/all_gardens.html',
        ]

    def get_all_gardens_with_records(self):
        raise NotImplementedError('Implement get_all_gardens_with_records')

    def get_user_gardens(self):
        profile = get_profile(self.request.user)
        user_gardens = profile.gardens.all()

        type = self.request.session.get('garden_type', 'all')
        if type and type != 'all':
            user_gardens = user_gardens.filter(type=type)
        return user_gardens

    def get_context_data(self, **kwargs):
        all_gardens = self.get_all_gardens_with_records()
        context = super(AllGardensView, self).get_context_data(**kwargs)
        context.update({
            'all_gardens_with_records': self.filter_gardens_by_type(all_gardens),
            'user_gardens': self.get_user_gardens(),
        })
        return context


class GardenMixin(RecordsMixin, SingleObjectMixin):
    model = Garden

    def get_object(self, queryset=None):
        object = super(GardenMixin, self).get_object(queryset=queryset)
        if self.request.user.has_perm('farmingconcrete.can_edit_any_garden'):
            return object
        elif object in get_profile(self.request.user).gardens.all():
            return object
        raise PermissionDenied

    def get_records(self):
        return super(GardenMixin, self).get_records().for_garden(self.object)


class GardenDetailAddRecordView(SuccessMessageFormMixin, LoginRequiredMixin,
                                MetricMixin, GardenMixin, FormView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GardenDetailAddRecordView, self).get(request, *args,
                                                          **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GardenDetailAddRecordView, self).post(request, *args,
                                                           **kwargs)

    def form_valid(self, form):
        self.record = form.save()
        return super(GardenDetailAddRecordView, self).form_valid(form)

    def get_initial(self):
        garden = self.object

        # Get a reasonable initial date for recorded
        try:
            recorded = self.get_records().order_by('-recorded')[0].recorded
        except Exception:
            recorded = date.today()

        initial = super(GardenDetailAddRecordView, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'garden': garden,
            'recorded': recorded,
        })
        return initial

    def get_success_url(self):
        return reverse(self.get_metric()['garden_detail_url_name'], kwargs={
            'pk': self.object.pk,
            'year': self.record.recorded.year,
        })

    def get_context_data(self, **kwargs):
        context = super(GardenDetailAddRecordView, self).get_context_data(**kwargs)
        garden = self.object
        records = self.get_records()
        context.update({
            'form': self.get_form(self.form_class),
            'garden': garden,
            'records': records.order_by('recorded'),
            'summary': self.get_metric_model().summarize(records),
        })
        return context


class GardenView(GardenMixin, LoginRequiredMixin, DetailView):

    def get_template_names(self):
        return [
            'metrics/%s/gardens/detail.html' % self.metric_model._meta.app_label,
        ]


class MetricGardenCSVView(LoginRequiredMixin, MetricMixin, GardenMixin,
                          CSVView):

    def get_fields(self):
        return ('recorded', 'added_by',)

    def get(self, request, *args, **kwargs):
        self.object = self.garden = self.get_object()
        return super(MetricGardenCSVView, self).get(request, *args, **kwargs)

    def get_filename(self):
        return '%s - %s - %s' % (
            self.garden.name,
            self.get_metric_name(),
            date.today().strftime('%Y-%m-%d'),
        )

    def get_rows(self):
        for record in self.get_records():
            def get_cell_value(record, field):
                value = getattr(record, field, None)
                if value is None:
                    return ''
                elif isinstance(value, Manager):
                    return ';'.join([str(instance) for instance in value.all()])
                return value
            yield dict(map(lambda f: (f, get_cell_value(record, f)), self.get_fields()))

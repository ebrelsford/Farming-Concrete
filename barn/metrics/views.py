from datetime import date, datetime, timedelta

from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DeleteView, DetailView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from accounts.utils import get_profile
from farmingconcrete.models import Garden
from generic.views import (DefaultYearMixin, LoginRequiredMixin,
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

    def get_context_data(self, **kwargs):
        context = super(MetricMixin, self).get_context_data(**kwargs)
        context.update({
            'index_url': self.get_index_url(),
            'metric_name': self.get_metric_name(),
            'metric': self.get_metric(),
            'page_type': 'data_entry',
        })
        return context


class RecordsMixin(DefaultYearMixin):
    """
    A mixin that aids in retrieving records (instances of models that derive
    from BaseMetricRecord) for a particular year.
    """

    def get_records(self):
        return self.metric_model.objects.for_year(self.get_year())


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
        perm = '%s.%s' % (meta.app_label, get_permission_codename('delete', meta))
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
        profile = get_profile(self.request.user)
        user_gardens = profile.gardens.all()
        return user_gardens

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        records = self.get_records()
        context.update({
            'summary': self.metric_model.summarize(records),
            'user_gardens': self.get_user_gardens().order_by('name'),
            'year': datetime.now().year,
        })
        return context

    def get_template_names(self):
        templates = [
            'metrics/%s/index.html' % self.metric_model._meta.app_label,
        ]
        if self.template_name:
            templates = [self.template_name] + templates
        return templates


class AllGardensView(DefaultYearMixin, LoginRequiredMixin,
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
        return profile.gardens.all()

    def get_context_data(self, **kwargs):
        context = super(AllGardensView, self).get_context_data(**kwargs)
        context.update({
            'user_gardens': self.get_user_gardens(),
            'year': self.get_year(),
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

    def get_initial_recorded(self):
        """
        Get a reasonable initial date for the recorded and recorded_start
        fields as appropriate.
        """
        today = date.today()
        try:
            start = self.get_records().order_by('-recorded')[0].recorded
        except Exception:
            start = None

        # Fall back to today if no records or recorded < today - ~6 mos
        if not start or (today - start).days > 180:
            start = today

        if self.has_recorded_start():
            if start == today:
                # Make room in range by pushing start back a bit
                start = today - timedelta(days=1)
                end = today
            else:
                # Leave start where it is, push end forward a week if we can
                end = min(today, start + timedelta(days=7))
            return {
                'recorded_start': start,
                'recorded': end,
            }
        else:
            return {
                'recorded': start,
            }

    def has_recorded_start(self):
        return 'recorded_start' in self.get_form_class()().fields.keys()

    def get_initial(self):
        initial = super(GardenDetailAddRecordView, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'garden': self.object,
        })
        initial.update(**self.get_initial_recorded())
        return initial

    def get_success_url(self):
        units = self.request.POST.get('weight_1', None)
        if not units:
            units = self.request.POST.get('volume_new_1', None)

        url = reverse(self.get_metric()['garden_detail_url_name'], kwargs={
            'pk': self.object.pk,
            'year': self.record.recorded.year,
        })
        if units:
            url += '?units=' + units
        return url

    def get_context_data(self, **kwargs):
        context = super(GardenDetailAddRecordView, self).get_context_data(**kwargs)
        garden = self.object
        records = self.get_records()
        context.update({
            'form': self.get_form(self.form_class),
            'garden': garden,
            'records': records.order_by('recorded'),
            'summary': self.get_metric_model().summarize(records),
            'year': self.get_year(),
        })
        return context


class GardenView(GardenMixin, LoginRequiredMixin, DetailView):

    def get_template_names(self):
        return [
            'metrics/%s/gardens/detail.html' % self.metric_model._meta.app_label,
        ]

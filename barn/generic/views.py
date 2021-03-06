from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, QueryDict
from django.views.generic.base import ContextMixin, View
from django.views.generic.dates import YearMixin
from django.views.generic.edit import FormMixin

from django_tablib.base import mimetype_map


class LoginRequiredMixin(object):
    """A mixin the requires a user to be logged in before access a view"""
    def dispatch(self, request, *args, **kwargs):
        @login_required(login_url=reverse('django.contrib.auth.views.login'))
        def wrapper(request, *args, **kwargs):
            return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                            **kwargs)
        return wrapper(request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """A mixin the requires a user to have permission to access a view"""
    def dispatch(self, request, *args, **kwargs):
        @permission_required(self.permission)
        def wrapper(request, *args, **kwargs):
            return super(PermissionRequiredMixin, self).dispatch(request,
                                                                 *args,
                                                                 **kwargs)
        return wrapper(request, *args, **kwargs)


class RememberPreviousPageMixin(object):
    query_string_exclude = ()

    def get(self, request, *args, **kwargs):
        self.previous_page = request.GET.get('previous', None)
        self.previous_query_string = self._get_previous_query_string(request.GET)
        return super(RememberPreviousPageMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # NB: these assume that you're putting them in your form
        self.previous_page = request.POST.get('previous', None)
        self.previous_query_string = self._get_previous_query_string(request.POST)
        return super(RememberPreviousPageMixin, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RememberPreviousPageMixin, self).get_context_data(**kwargs)
        context.update({
            'previous_page': self.previous_page,
            'previous_query_string': self.previous_query_string,
        })
        return context

    def _get_previous_query_string(self, params):
        query_string = params.get('previous_query_string', '')

        # remove anything in exclude
        query_dict = QueryDict(query_string).copy()
        for excluded in self.query_string_exclude:
            try:
                del query_dict[excluded]
            except KeyError:
                pass
        return query_dict.urlencode()


class RedirectToPreviousPageMixin(RememberPreviousPageMixin, FormMixin):
    def get_success_url(self):
        return '%s?%s&%s' % (
            self.previous_page,
            self.previous_query_string,
            self.get_success_querystring(),
        )

    def get_success_querystring(self):
        return ''


class InitializeUsingGetMixin(FormMixin):
    def get_initial(self):
        initial = super(InitializeUsingGetMixin, self).get_initial()
        fields = self.get_form_class()().fields.keys()
        for field in fields:
            try:
                if field in initial and initial[field] is not None: continue
                initial[field] = self.request.GET[field]
            except Exception:
                continue
        return initial


class SuccessMessageFormMixin(FormMixin):

    def form_valid(self, form):
        self.add_success_message()
        return super(SuccessMessageFormMixin, self).form_valid(form)

    def add_success_message(self):
        messages.success(self.request, self.get_success_message())

    def get_success_message(self):
        return self.success_message


class TitledPageMixin(ContextMixin):

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super(TitledPageMixin, self).get_context_data(**kwargs)
        context.update({
            'title': self.get_title(),
        })
        return context


class DefaultYearMixin(YearMixin):

    def get_default_year(self):
        return datetime.now().year

    def get_year(self):
        try:
            year = int(super(DefaultYearMixin, self).get_year())
            return year or self.get_default_year()
        except Exception:
            return self.get_default_year()


class TablibView(View):
    format = 'csv'
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def get_dataset(self):
        """Get the dataset"""
        raise NotImplementedError('Implement TablibView.get_dataset()')

    def get_filename(self):
        """Get the filename for the file"""
        return 'download'

    def get_format(self):
        """Get the format for the file"""
        return self.format

    def render_to_response(self):
        response = self.response_class(
            getattr(self.get_dataset(), self.get_format()),
            content_type=mimetype_map.get(self.get_format(), 'application/octet-stream')
        )
        response['Content-Disposition'] = ('attachment; filename="%s.%s"' % (
            self.get_filename(),
            self.get_format(),
        ))
        return response

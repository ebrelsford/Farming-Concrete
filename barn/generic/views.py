from django.contrib.auth.decorators import login_required, permission_required
from django.http import QueryDict
from django.views.generic.edit import FormMixin


class LoginRequiredMixin(object):
    """A mixin the requires a user to be logged in before access a view"""
    def dispatch(self, request, *args, **kwargs):
        @login_required
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
        print initial
        return initial

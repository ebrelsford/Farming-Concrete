from django.contrib.auth.decorators import login_required, permission_required

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

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView

from generic.views import LoginRequiredMixin

from .forms import UserForm
from .models import GardenMembership
from .utils import is_admin


class AccountDetailsView(UpdateView):
    form_class = UserForm
    template_name = 'accounts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailsView, self).get_context_data(**kwargs)
        context['page_type'] = 'account'
        return context

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse('account_details')


class AddAdminView(LoginRequiredMixin, DetailView):
    """Add a user as admin for a garden."""
    model = GardenMembership

    def add_admin(self, membership):
        membership.is_admin = True
        membership.save()

    def get_success_message(self, membership):
        return 'Successfully added %s as admin' % (
            membership.user_profile.user.username,
        )

    def get(self, request, *args, **kwargs):
        membership = self.get_object()

        if not is_admin(request.user, membership.garden):
            raise PermissionDenied

        self.add_admin(membership)
        messages.success(request, self.get_success_message(membership))
        return HttpResponse('OK', content_type='text/plain')


class DeleteAdminView(LoginRequiredMixin, DetailView):
    """Remove a user as admin for a garden."""
    model = GardenMembership

    def delete_admin(self, membership):
        membership.is_admin = False
        membership.save()

    def get_success_message(self, membership):
        return 'Successfully removed %s as admin' % (
            membership.user_profile.user.username,
        )

    def get(self, request, *args, **kwargs):
        membership = self.get_object()

        if not is_admin(request.user, membership.garden):
            raise PermissionDenied

        self.delete_admin(membership)
        messages.success(request, self.get_success_message(membership))
        return HttpResponse('OK', content_type='text/plain')


class DeleteMemberView(LoginRequiredMixin, DetailView):
    """Remove a user from a garden."""
    model = GardenMembership

    def get_success_message(self, membership):
        return 'Successfully removed %s' % membership.user_profile.user.username

    def get(self, request, *args, **kwargs):
        membership = self.get_object()

        if not is_admin(request.user, membership.garden):
            raise PermissionDenied

        membership.delete()
        messages.success(request, self.get_success_message(membership))
        return HttpResponse('OK', content_type='text/plain')

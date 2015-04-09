from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, FormView, UpdateView

from generic.views import LoginRequiredMixin
from templated_emails.utils import send_templated_email

from farmingconcrete.views import GardenGroupAdminPermissionMixin
from .forms import InviteForm, UserForm
from .models import GardenMembership, GardenGroupUserMembership
from .utils import get_profile


class AccountDetailsView(LoginRequiredMixin, UpdateView):
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

        if not membership.garden.is_admin(request.user):
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

        if not membership.garden.is_admin(request.user):
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

        if not membership.garden.is_admin(request.user):
            raise PermissionDenied

        membership.delete()
        messages.success(request, self.get_success_message(membership))
        return HttpResponse('OK', content_type='text/plain')


class InviteMemberView(FormView):
    form_class = InviteForm
    template_name = 'accounts/garden_member_invite.html'

    def send_invite(self, email, garden):
        profile = get_profile(self.request.user)
        if profile.invite_count > settings.MAX_INVITES and not self.request.user.is_staff:
            raise PermissionDenied
        # TODO Tracking *who* invited *whom* could be nice, too
        profile.invite_count += 1
        profile.save()

        send_templated_email(
            [email,],
            'emails/invite',
            { 
                'base_url': settings.BASE_URL,
                'garden': garden,
                'inviter': self.request.user,
            }
        )

    def form_valid(self, form):
        self.send_invite(form.cleaned_data['email'], form.cleaned_data['garden'])
        return super(InviteMemberView, self).form_valid(form)

    def get_success_url(self):
        return reverse('gardenmemberships_invite')


class DeleteGardenGroupMemberView(LoginRequiredMixin,
                                  GardenGroupAdminPermissionMixin, DetailView):
    """Remove a user from a garden group."""
    model = GardenGroupUserMembership

    def get_success_message(self, membership):
        return 'Successfully removed %s' % membership.user_profile.user.username

    def get(self, request, *args, **kwargs):
        membership = self.get_object()
        if not super(DeleteGardenGroupMemberView, self).check_permission(membership.group):
            raise PermissionDenied
        membership.delete()
        messages.success(request, self.get_success_message(membership))
        return HttpResponse('OK', content_type='text/plain')

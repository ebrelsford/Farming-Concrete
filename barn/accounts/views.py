from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from braces.views import FormValidMessageMixin

from generic.views import LoginRequiredMixin
from templated_emails.utils import send_templated_email

from farmingconcrete.models import GardenGroup
from farmingconcrete.views import GardenGroupAdminPermissionMixin
from .forms import AddGardenGroupAdminForm, InviteForm, UserForm
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

    def add_garden_admins(self, group, deleted_user):
        """If the group no longer has admins, promote all garden admins."""
        memberships = GardenGroupUserMembership.objects.filter(group=group)
        if memberships.exists():
            return
        new_admins = chain(*[g.admins() for g in group.active_gardens()])

        # Don't re-add the just deleted user
        new_admins = filter(lambda a: a != deleted_user, new_admins)

        # Add admins
        for user in new_admins:
            group.add_admin(user)
        if new_admins:
            messages.info(self.request, ('You deleted the last admin, so we '
                                         'added all member garden admins'))

    def get_success_message(self, membership):
        return 'Successfully removed %s' % membership.user_profile.user.username

    def get(self, request, *args, **kwargs):
        membership = self.get_object()
        if not super(DeleteGardenGroupMemberView, self).check_permission(membership.group):
            raise PermissionDenied
        membership.delete()
        self.add_garden_admins(membership.group, membership.user_profile.user)
        messages.success(request, self.get_success_message(membership))
        return HttpResponse('OK', content_type='text/plain')


class AddGardenGroupAdminView(GardenGroupAdminPermissionMixin, 
                              LoginRequiredMixin, FormValidMessageMixin,
                              SingleObjectMixin, FormView):
    """Add a user as admin for a garden group."""
    form_class = AddGardenGroupAdminForm
    form_valid_message = 'Successfully updated group'
    model = GardenGroup

    def add_admins(self, group, garden_members):
        for garden_member in garden_members:
            admin, created = GardenGroupUserMembership.objects.get_or_create(
                group=group,
                user_profile=garden_member.user_profile,
            )
            admin.is_admin = True
            admin.save()

    def get_form_kwargs(self):
        kwargs = super(AddGardenGroupAdminView, self).get_form_kwargs()
        kwargs['group'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        group = self.get_object()

        if not self.check_permission(group):
            raise PermissionDenied
        garden_members = form.cleaned_data['users']
        self.add_admins(group, garden_members)
        return super(AddGardenGroupAdminView, self).form_valid(form)

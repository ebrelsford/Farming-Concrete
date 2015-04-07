from datetime import datetime
import geojson
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import (CreateView, DetailView, UpdateView,
                                  TemplateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from braces.views import JSONResponseMixin, MessageMixin
from templated_emails.utils import send_templated_email

from accounts.models import GardenMembership
from accounts.utils import get_profile
from generic.views import (DefaultYearMixin, LoginRequiredMixin,
                           SuccessMessageFormMixin)
from metrics.registry import registry
from middleware.http import Http403
from .geo import garden_collection
from .forms import GardenForm, GardenGroupForm
from .models import Garden, GardenGroup, GardenGroupMembership, GardenType


class UserGardensMixin(object):

    def get_user_gardens(self):
        user = self.request.user
        try:
            if user.is_authenticated():
                profile = get_profile(user)
                return profile.gardens.all().order_by('name')
        except Exception:
            return []

    def get_context_data(self, **kwargs):
        context = super(UserGardensMixin, self).get_context_data(**kwargs)
        context['user_gardens'] = self.get_user_gardens()
        return context


class IndexView(UserGardensMixin, TemplateView):
    template_name = 'farmingconcrete/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_type'] = 'index'
        return context


class GardenDetails(DefaultYearMixin, LoginRequiredMixin, UserGardensMixin,
                    DetailView):
    model = Garden
    template_name = 'farmingconcrete/gardens/detail.html'

    def get_context_data(self, **kwargs):
        context = super(GardenDetails, self).get_context_data(**kwargs)

        garden = self.object
        user = self.request.user
        if not user.has_perm('can_edit_any_garden'):
            if garden not in self.get_user_gardens():
                raise Http403
        context.update({
            'garden_list': (garden,),
            'garden_ids': (garden.pk,),
            'page_type': 'data_entry',
            'year': self.get_year(),
        })
        return context


class UserGardens(LoginRequiredMixin, UserGardensMixin, ListView):
    context_object_name = 'garden_list'
    model = Garden
    template_name = 'farmingconcrete/gardens/detail.html'

    def get_queryset(self):
        return self.get_user_gardens()

    def get_context_data(self, **kwargs):
        if not self.get_queryset().exists():
            add_url = reverse('farmingconcrete_gardens_add')
            message = """
                Whoa now, you don't have any gardens! You should
                <a href="%s">add a new garden</a> before you add data.
            """ % (add_url,)
            messages.add_message(self.request, messages.WARNING, message)
        context = super(UserGardens, self).get_context_data(**kwargs)
        context['garden_ids'] = self.get_queryset().values_list('pk', flat=True)
        context['page_type'] = 'data_entry'
        return context


class AddUserGardenMixin(object):

    def add_garden_to_user(self, garden):
        user = self.request.user
        if not (user and user.is_authenticated()):
            return

        # Make sure user isn't already in garden
        existing_membership = GardenMembership.objects.filter(
            garden=garden,
            user_profile__user=user
        )
        if existing_membership.exists():
            return

        # Make user the admin if they're the first
        is_first = not GardenMembership.objects.filter(garden=garden).exists()
        garden_membership = GardenMembership(
            garden=garden,
            user_profile=get_profile(user),
            is_admin=is_first,
            added_by=user,
        )
        garden_membership.save()


class GardenFormMixin(FormMixin):
    form_class = GardenForm
    model = Garden

    def get_form_kwargs(self):
        kwargs = super(GardenFormMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        try:
            groups = self.object.groups()
        except Exception:
            groups = None
        initial = super(GardenFormMixin, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'groups': groups,
        })
        return initial


class CreateGardenView(LoginRequiredMixin, AddUserGardenMixin, GardenFormMixin,
                       SuccessMessageFormMixin, CreateView):

    def get_success_message(self):
        return 'Successfully added %s' % self.object

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        """Add the garden to the user's gardens."""
        garden = self.object = form.save()
        self.add_garden_to_user(garden)
        self.add_success_message()
        return HttpResponseRedirect(self.get_success_url())


class UpdateGardenView(LoginRequiredMixin, SuccessMessageFormMixin,
                       GardenFormMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        if not self.get_object().is_member(request.user):
            raise PermissionDenied
        return super(UpdateGardenView, self).get(request, *args, **kwargs)

    def get_success_message(self):
        return 'Successfully edited %s' % self.object

    def get_success_url(self):
        return reverse('farmingconcrete_garden_details',
                       kwargs={ 'pk': self.object.pk })


class GardenSuggestionView(LoginRequiredMixin, ListView):
    model = Garden
    template_name = 'farmingconcrete/gardens/suggestions.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        try:
            name = self.request.GET['name']
            qs = self.model.objects.filter(name__icontains=name)
        except Exception:
            pass
        return qs.order_by('name')[:10]


class AddSuggestedGardenView(LoginRequiredMixin, AddUserGardenMixin, DetailView):
    model = Garden

    def add_suggested(self):
        garden = self.get_object()
        self.add_garden_to_user(garden)
        messages.success(self.request, 'Added %s to your gardens' % garden.name)


    def get(self, request, *args, **kwargs):
        self.add_suggested()
        return HttpResponseRedirect(reverse('home'))


def gardens_geojson(request):
    """Get GeoJSON for requested gardens"""

    gardens = Garden.objects.exclude(latitude=None, longitude=None)

    ids = request.GET.get('ids', None)
    cropcount = request.GET.get('cropcount', None)
    gardenid = request.GET.get('gardenid', None)
    harvestcount = request.GET.get('harvestcount', None)
    metric = request.GET.get('metric', None)
    participating = request.GET.get('participating', None)
    type = request.GET.get('gardentype', None)
    borough = request.GET.get('borough', None)
    year = request.GET.get('year', datetime.now().year)
    user_gardens = request.GET.get('user_gardens', False)

    if metric:
        records = registry[metric]['model'].objects.for_year(year)
        ids = records.values_list('garden__pk', flat=True)

    if user_gardens:
        user = request.user
        try:
            if user.is_authenticated():
                profile = get_profile(user)
                ids = profile.gardens.all().values_list('pk', flat=True)
        except Exception:
            pass

    if gardenid:
        ids = [gardenid,]

    if ids:
        try:
            ids = ids.split(',')
        except Exception:
            pass
        gardens = gardens.filter(id__in=ids)
    if type and type != 'all':
        gardens = gardens.filter(type__short_name=type)
    if borough:
        gardens = gardens.filter(borough=borough)

    if cropcount and cropcount != 'no':
        gardens = gardens.filter(box__patch__added__year=year)
    elif harvestcount and harvestcount != 'no':
        gardens = gardens.filter(gardener__harvest__harvested__year=year)
    elif participating and participating != 'no':
        gardens = gardens.filter(Q(box__patch__added__year=year) |
                                 Q(gardener__harvest__harvested__year=year))

    gardens = gardens.distinct()
    return HttpResponse(geojson.dumps(garden_collection(gardens)),
                        content_type='application/json')


def _get_garden_type(short_name):
    types = GardenType.objects.filter(short_name=short_name)
    if types.count() > 0:
        return types[0]

    return 'all'


class UserGardenLeaveView(LoginRequiredMixin, DetailView):
    model = Garden
    template_name = 'farmingconcrete/gardens/user_garden_leave.html'


class UserGardenLeaveConfirmedView(LoginRequiredMixin, DetailView):
    model = Garden
    template_name = 'farmingconcrete/gardens/user_garden_leave.html'

    def remove_garden_from_user(self, garden):
        user = self.request.user
        if user and user.is_authenticated():
            GardenMembership.objects.filter(
                garden=garden,
                user_profile=get_profile(user)
            ).delete()

    def get(self, request, *args, **kwargs):
        garden = self.get_object()
        self.remove_garden_from_user(garden)
        messages.success(self.request, 'Removed %s from your gardens' % garden.name)
        return HttpResponseRedirect(reverse('home'))


class GardenGroupMixin(SingleObjectMixin):
    model = GardenGroup

    def check_permission(self, group):
        """
        Can the user see the garden group's page? Only if they are:
         * admin
         * admin of the group
         * admin of a garden in the group
        """
        user = self.request.user

        # Admins can see anything
        if user.has_perm('can_edit_any_garden'):
            return True

        # Only allow access to users who are admins of this group or of a
        # member garden
        if group.is_admin(user) or group.is_admin_of_member_garden(user):
            return True
        return False

    def get_object(self, queryset=None):
        object = super(GardenGroupMixin, self).get_object(queryset=queryset)
        if not self.check_permission(object):
            raise PermissionDenied
        return object


class GardenGroupDetailView(GardenGroupMixin, LoginRequiredMixin, DetailView):
    pass


class CreateGardenGroupView(LoginRequiredMixin, CreateView):
    form_class = GardenGroupForm
    model = GardenGroup
    template_name = 'farmingconcrete/gardengroup/gardengroup_form.html'

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'added_by': self.request.user,
            'updated_by': self.request.user,
        })
        return initial

    def get_gardengroup(self, name, user):
        return GardenGroup.objects.get_or_create(
            name=name,
            added_by=user,
        )

    def form_valid(self, form):
        name = form.cleaned_data['name']
        gardengroup, created = self.get_gardengroup(name, self.request.user)
        self.object = gardengroup
        return HttpResponse(json.dumps({
            'name': gardengroup.name,
            'pk': gardengroup.pk,
        }), content_type='application/json')


class UpdateGardenGroupView(LoginRequiredMixin, SuccessMessageFormMixin,
                            UpdateView):
    form_class = GardenGroupForm
    model = GardenGroup
    template_name = 'farmingconcrete/gardengroup/update.html'

    def get(self, request, *args, **kwargs):
        if not (request.user.has_perm('can_edit_any_garden') or
                self.get_object().is_admin(request.user)):
            raise PermissionDenied
        return super(UpdateGardenGroupView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'updated_by': self.request.user,
        })
        return initial

    def get_success_message(self):
        return 'Successfully edited %s' % self.object

    def get_success_url(self):
        return reverse('farmingconcrete_gardengroup_detail',
                       kwargs={ 'pk': self.object.pk })


class CheckGardenGroupMembershipAccess(LoginRequiredMixin, JSONResponseMixin,
                                       DetailView):
    model = GardenGroup

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            garden = Garden.objects.get(pk=request.GET.get('garden', None))
        except (Garden.DoesNotExist, ValueError):
            garden = None
        user = User.objects.get(pk=request.GET.get('user', None))
        context = {
            'can_join': self.object.can_join(garden=garden, user=user),
            'group': {
                'pk': self.object.pk,
                'name': self.object.name,
            },
        }
        return self.render_json_response(context)


class AcceptGardenGroupMembership(GardenGroupMixin, MessageMixin, 
                                  LoginRequiredMixin, JSONResponseMixin,
                                  DetailView):

    def approve_membership(self, garden, group):
        memberships = GardenGroupMembership.by_status.pending_requested().filter(
            garden=garden,
            group=group,
        )
        memberships.update(status=GardenGroupMembership.ACTIVE)
        return memberships

    def remove_extra_memberships(self, garden, group):
        memberships = GardenGroupMembership.by_status.any().filter(
            garden=garden,
            group=group,
        )
        if memberships.count() > 1:
            GardenGroupMembership.by_status.any().filter(
                pk__in=[m.pk for m in memberships.order_by('added')[1:]],
            ).delete()

    def check_permission(self, group):
        user = self.request.user
        return group.is_admin(user) or user.has_perm('can_edit_any_garden')

    def get(self, request, garden_pk=None, *args, **kwargs):
        group = self.object = self.get_object()
        garden = Garden.objects.get(pk=garden_pk)

        self.approve_membership(garden, group)
        self.remove_extra_memberships(garden, group)
        self.messages.success('Successfully approved %s' % garden.name)

        return redirect('farmingconcrete_gardengroup_detail', pk=self.object.pk)


class RequestGardenGroupMembership(LoginRequiredMixin, JSONResponseMixin,
                                   DetailView):
    model = GardenGroup

    def email_group_admins(self, garden, user, membership):
        send_templated_email(
            [admin.email for admin in self.object.admins()],
            'emails/request_gardengroup_membership', {
                'base_url': settings.BASE_URL,
                'garden': garden,
                'group': self.object,
                'membership': membership,
                'user': user,
            }
        )

    def add_requested_membership(self, garden, user):
        membership = GardenGroupMembership(
            added_by=user,
            garden=garden,
            group=self.object,
            status=GardenGroupMembership.PENDING_REQUESTED,
        )
        membership.save()
        return membership

    def failure(self, group, message):
        context = {
            'request_sent': False,
            'message': message,
            'group': {
                'pk': group.pk,
                'name': group.name,
            },
        }
        return self.render_json_response(context)

    def success(self, group):
        context = {
            'request_sent': True,
            'group': {
                'pk': group.pk,
                'name': group.name,
            },
        }
        return self.render_json_response(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            garden = Garden.objects.get(pk=request.GET.get('garden', None))
        except (Garden.DoesNotExist, ValueError):
            msg = ('Please save garden before requesting permission to join a '
                   'group.')
            return self.failure(self.object, msg)
        user = User.objects.get(pk=request.GET.get('user', None))
        membership = self.add_requested_membership(garden, user)
        self.email_group_admins(garden, user, membership)
        return self.success(self.object)

import geojson
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import (CreateView, DetailView, View, UpdateView,
                                  TemplateView)
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from accounts.models import UserProfile
from generic.views import (DefaultYearMixin, LoginRequiredMixin,
                           PermissionRequiredMixin, RememberPreviousPageMixin,
                           SuccessMessageFormMixin)
from metrics.cropcount.models import Patch
from metrics.harvestcount.models import Harvest
from metrics.registry import registry
from middleware.http import Http403
from .geo import garden_collection
from .forms import GardenForm, VarietyForm
from .models import Garden, GardenGroup, GardenType, Variety
from .utils import get_variety


def _harvests(year=settings.FARMINGCONCRETE_YEAR):
    """Get current harvests"""
    return Harvest.objects.filter(harvested__year=year)


def _patches(year=settings.FARMINGCONCRETE_YEAR):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)


class AddYearToSessionMixin(View):

    def add_year_to_session(self, request):
        year = (self.kwargs.get('year', None)
                or request.session.get('year', None)
                or settings.FARMINGCONCRETE_YEAR)
        request.session['year'] = self.kwargs['year'] = year

    def dispatch(self, request, *args, **kwargs):
        self.add_year_to_session(request)
        return super(AddYearToSessionMixin, self).dispatch(request, *args,
                                                           **kwargs)


class UserGardensMixin(object):

    def get_user_gardens(self):
        user = self.request.user
        try:
            if user.is_authenticated():
                profile = user.get_profile()
                return profile.gardens.all().order_by('name')
        except Exception:
            return []

    def get_context_data(self, **kwargs):
        context = super(UserGardensMixin, self).get_context_data(**kwargs)
        context['user_gardens'] = self.get_user_gardens()
        return context


class IndexView(AddYearToSessionMixin, UserGardensMixin, TemplateView):
    template_name = 'farmingconcrete/index.html'


class FarmingConcreteGardenDetails(LoginRequiredMixin, AddYearToSessionMixin,
                                   UserGardensMixin, DetailView):
    model = Garden
    template_name = 'farmingconcrete/gardens/detail.html'

    def get_context_data(self, **kwargs):
        context = super(FarmingConcreteGardenDetails, self).get_context_data(**kwargs)

        garden = self.object
        user = self.request.user
        if not user.has_perm('can_edit_any_garden'):
            if garden not in self.get_user_gardens():
                raise Http403
        return context


class AddUserGardenMixin(object):

    def add_garden_to_user(self, garden):
        user = self.request.user
        if user and user.is_authenticated():
            try:
                profile = user.get_profile()
            except Exception:
                profile = UserProfile(user=user)
                profile.save()
            profile.gardens.add(garden)


class GardenFormMixin(FormMixin):
    form_class = GardenForm
    model = Garden

    def get_initial(self):
        initial = super(GardenFormMixin, self).get_initial()
        initial.update({
            'added_by': self.request.user,
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

    def get_success_message(self):
        return 'Successfully edited %s' % self.object

    def get_success_url(self):
        return reverse('home')


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


@login_required
def account(request):
    return render_to_response('farmingconcrete/account.html', {},
                              context_instance=RequestContext(request))


@login_required
def switch_garden_type(request, type='all'):
    next = request.GET['next']
    request.session['garden_type'] = type = _get_garden_type(type)
    return redirect(next)


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
    year = request.GET.get('year', settings.FARMINGCONCRETE_YEAR)
    user_gardens = request.GET.get('user_gardens', False)

    if metric:
        records = registry[metric]['model'].objects.for_year(year)
        ids = records.values_list('garden__pk', flat=True)

    if user_gardens:
        user = request.user
        try:
            if user.is_authenticated():
                profile = user.get_profile()
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
                        mimetype='application/json')


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
            try:
                profile = user.get_profile()
            except Exception:
                profile = UserProfile(user=user)
                profile.save()
            profile.gardens.remove(garden)

    def get(self, request, *args, **kwargs):
        garden = self.get_object()
        self.remove_garden_from_user(garden)
        messages.success(self.request, 'Removed %s from your gardens' % garden.name)
        return HttpResponseRedirect(reverse('home'))


class VarietyPickerListView(LoginRequiredMixin, RememberPreviousPageMixin,
                            ListView):
    query_string_exclude = ('variety', 'variety_text')

    def get_queryset(self):
        return (Variety.objects.filter(needs_moderation=False) |
                self.request.user.farmingconcrete_variety_added.all())


class GardenGroupDetailView(LoginRequiredMixin, DetailView):
    model = GardenGroup


class FarmingConcreteYearMixin(DefaultYearMixin):

    def get_year(self):
        return self.request.session['year']

    def get_default_year(self):
        return settings.FARMINGCONCRETE_YEAR


class CreateVarietyView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    form_class = VarietyForm
    model = Variety
    permission = 'farmingconcrete.add_variety'
    template_name = 'farmingconcrete/variety/variety_form.html'

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'added_by': self.request.user,
            'updated_by': self.request.user,
        })
        return initial

    def form_valid(self, form):
        name = form.cleaned_data['name']
        variety, created = get_variety(name, self.request.user)
        self.object = variety
        return HttpResponse(json.dumps({
            'name': variety.name,
            'pk': variety.pk,
        }), content_type='application/json')

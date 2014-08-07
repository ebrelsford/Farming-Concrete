from datetime import datetime
import geojson

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (CreateView, DetailView, UpdateView,
                                  TemplateView)
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from accounts.models import GardenMembership
from accounts.utils import get_profile, is_member
from generic.views import (DefaultYearMixin, LoginRequiredMixin,
                           SuccessMessageFormMixin)
from metrics.registry import registry
from middleware.http import Http403
from .geo import garden_collection
from .forms import GardenForm
from .models import Garden, GardenGroup, GardenType


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

    def get_initial(self):
        try:
            groups = self.object.gardengroup_set.all()
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
        if not is_member(request.user, self.get_object()):
            raise PermissionDenied
        return super(UpdateGardenView, self).get(request, *args, **kwargs)

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
            GardenMembership.objects.filter(
                garden=garden,
                user_profile=get_profile(user)
            ).delete()

    def get(self, request, *args, **kwargs):
        garden = self.get_object()
        self.remove_garden_from_user(garden)
        messages.success(self.request, 'Removed %s from your gardens' % garden.name)
        return HttpResponseRedirect(reverse('home'))


class GardenGroupDetailView(LoginRequiredMixin, DetailView):
    model = GardenGroup

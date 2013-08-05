from datetime import date
import json

import unicodecsv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic.edit import CreateView

from barn.mobile import is_mobile
from farmingconcrete.decorators import garden_type_aware, in_section, year_in_session
from farmingconcrete.models import Garden, Variety
from farmingconcrete.forms import GardenForm, FindGardenForm
from generic.views import InitializeUsingGetMixin, LoginRequiredMixin, PermissionRequiredMixin, RedirectToPreviousPageMixin
from models import Gardener, Harvest
from harvestcount.forms import AutocompleteHarvestForm, GardenerForm, MobileHarvestForm

from middleware.http import Http403


def _harvests(year=settings.FARMINGCONCRETE_YEAR):
    """Get current harvests"""
    return Harvest.objects.filter(harvested__year=year)


@login_required
@garden_type_aware
@in_section('harvestcount')
@year_in_session
def index(request, year=None):
    garden_type = request.session['garden_type']

    harvests = _harvests(year=year)
    if garden_type != 'all':
        harvests = harvests.filter(gardener__garden__type=garden_type).distinct()

    gardeners = Gardener.objects.filter(harvest__in=harvests).distinct()
    gardens = Garden.objects.filter(gardener__in=gardeners).distinct()

    return render_to_response('harvestcount/index.html', {
        'gardens': gardens.count(),
        'gardeners': gardeners.count(),
        'weight': harvests.aggregate(t=Sum('weight'))['t'],
        'plant_types': harvests.values('variety__id').distinct().count(),
        'recent_harvests': harvests.order_by('-added')[:3],
    }, context_instance=RequestContext(request))


@login_required
@garden_type_aware
@in_section('harvestcount')
@year_in_session
def add_garden(request, year=None):
    if request.method == 'POST':
        form = GardenForm(request.POST, user=request.user)
        if form.is_valid():
            garden = form.save()
            return redirect(garden_details, id=garden.id, year=year)

        find_garden_form = FindGardenForm(request.POST)
        if find_garden_form.is_valid():
            garden = find_garden_form.cleaned_data['garden']
            return redirect(garden_details, id=garden.id, year=year)
    else:
        form = GardenForm(user=request.user)
        find_garden_form = FindGardenForm(user=request.user)

    return render_to_response('harvestcount/gardens/add.html', {
        'form': form,
        'find_garden_form': find_garden_form,
    }, context_instance=RequestContext(request))


@login_required
@in_section('harvestcount')
@year_in_session
def garden_details(request, id=None, year=None):
    """Show details for a garden, let user add harvests"""
    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('farmingconcrete.can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    if request.method == 'POST':
        form = AutocompleteHarvestForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(garden_details, id=id, year=year)
    else:
        try:
            most_recent_harvest = Harvest.objects.filter(
                gardener__garden=garden,
                added__year=year,
            ).order_by('-added')[0]
            harvested = most_recent_harvest.harvested
            gardener_id = most_recent_harvest.gardener.id
        except:
            harvested = date.today()
            gardener_id = None

        form = AutocompleteHarvestForm(initial={
            'garden': garden,
            'harvested': harvested,
            'gardener': gardener_id,
        }, user=request.user)

    harvests = _harvests(year=year).filter(gardener__garden=garden)
    return render_to_response('harvestcount/gardens/detail.html', {
        'garden': garden,
        'harvests': harvests.order_by('harvested', 'gardener__name'),
        'form': form,
        'weight': harvests.aggregate(t=Sum('weight'))['t'],
        'plant_types': harvests.values('variety__id').distinct().count(),
        'plants': None,
    }, context_instance=RequestContext(request))


@login_required
@garden_type_aware
@in_section('harvestcount')
@year_in_session
def user_gardens(request, year=None):
    """Show the user's gardens"""
    type = request.session['garden_type']

    profile = request.user.get_profile()
    user_gardens = profile.gardens.all()
    if type != 'all':
        user_gardens = user_gardens.filter(type=type)

    return render_to_response('harvestcount/gardens/user_gardens.html', {
        'user_gardens': user_gardens.order_by('name'),
        'user_garden_ids': user_gardens.values_list('id', flat=True),
    }, context_instance=RequestContext(request))


@login_required
@garden_type_aware
@in_section('harvestcount')
@year_in_session
def all_gardens(request, year=None):
    """Show all harvested gardens"""
    type = request.session['garden_type']

    gardens = Garden.objects.filter(gardener__harvest__harvested__year=year).distinct()
    profile = request.user.get_profile()
    user_gardens = profile.gardens.all()
    if type != 'all':
        gardens = gardens.filter(type=type)
        user_gardens = user_gardens.filter(type=type)

    return render_to_response('harvestcount/gardens/all_gardens.html', {
        'gardens': gardens.order_by('name'),
        'user_gardens': user_gardens,
    }, context_instance=RequestContext(request))


@login_required
@in_section('harvestcount')
@year_in_session
def delete_harvest(request, id, year=None):
    harvest = get_object_or_404(Harvest, pk=id)
    garden_id = harvest.gardener.garden.id
    harvest.delete()
    return redirect(garden_details, id=garden_id, year=year)


@login_required
@year_in_session
def quantity_for_last_harvest(request, id=None, year=None):
    garden = id
    gardener = request.GET.get('gardener', None)
    variety = request.GET.get('variety', None)

    result = {
        'plants': '',
        'area': '',
    }
    if garden and gardener and variety:
        garden = get_object_or_404(Garden, pk=garden)
        if not request.user.has_perm('can_edit_any_garden'):
            profile = request.user.get_profile()
            if garden not in profile.gardens.all():
                return HttpResponseForbidden()
        try:
            harvest = Harvest.objects.filter(gardener__garden=garden, gardener__name=gardener, variety__name=variety).order_by('-harvested')[0]
        except IndexError:
            raise Http404

        result['plants'] = harvest.plants
        try:
            result['area'] = float(harvest.area)
        except:
            result['area'] = None
    return HttpResponse(json.dumps(result), mimetype='application/json')


@login_required
@year_in_session
def download_garden_harvestcount_as_csv(request, id, year=None):
    garden = get_object_or_404(Garden, pk=id)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s Harvest Count (%s).csv"' % (garden.name, date.today().strftime('%m-%d-%Y'))

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['gardener', 'plant type', 'pounds', 'number of plants', 'area (square feet)', 'date'])

    harvests = _harvests(year=year).filter(gardener__garden=garden).distinct()
    for harvest in harvests.order_by('gardener__name', 'variety__name'):
        writer.writerow([
            harvest.gardener.name,
            harvest.variety.name,
            harvest.weight,
            harvest.plants or '',
            harvest.area or '',
            harvest.harvested.strftime('%m-%d-%Y')
        ])

    return response


class HarvestAddView(LoginRequiredMixin, InitializeUsingGetMixin, CreateView):
    template_name = 'harvestcount/harvests/add.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Prepare initial and object variables before dispatching.
        """
        self.garden = get_object_or_404(Garden, pk=kwargs['id'])
        self.year = kwargs['year']
        self.is_mobile = is_mobile(request)

        # initialize initial, as the same values will be stored in the object
        self.initial = self._initial_init(request, self.garden)
        self.variety = self.initial['variety']
        self.gardener = self.initial['gardener']

        self.initial['garden'] = self.garden.pk

        return super(HarvestAddView, self).dispatch(request, *args, **kwargs)

    def _initial_init(self, request, garden):
        """
        Initialize the initial dict sent to the form.
        """
        area = None
        gardener = None
        harvested = date.today()
        plants = None
        variety = None

        try:
            variety_id = request.GET['variety']
            variety = Variety.objects.get(id=variety_id)
        except Exception:
            pass

        try:
            gardener_id = request.GET['gardener']
            gardener = Gardener.objects.get(id=gardener_id)
        except Exception:
            pass

        if not gardener:
            # if user is a gardener at this garden, use that
            try:
                current_gardener = request.user.get_profile().gardener
                if current_gardener.garden == garden:
                    gardener = current_gardener
            except Exception:
                pass

        if not gardener:
            # finally, if someone added a harvest here recently, use that
            try:
                most_recent_harvest = Harvest.objects.filter(
                    gardener__garden=garden,
                ).order_by('-added')[0]
                harvested = most_recent_harvest.harvested
                gardener = most_recent_harvest.gardener.pk
            except Exception:
                pass

        if variety and gardener and not request.GET.get('plants', None):
            try:
                most_recent_variety_harvest = Harvest.objects.filter(
                    gardener=gardener,
                    variety=variety,
                ).order_by('-added')[0]
                area = most_recent_variety_harvest.area
                plants = most_recent_variety_harvest.plants
            except Exception:
                pass

        return {
            'area': area,
            'gardener': gardener,
            'harvested': harvested,
            'plants': plants,
            'variety': variety,
        }

    def get_context_data(self, **kwargs):
        context = super(HarvestAddView, self).get_context_data(**kwargs)
        context.update({
            'garden': self.garden,
            'gardener': self.gardener,
            'variety': self.variety,
        })
        return context

    def get_form_class(self):
        if self.is_mobile:
            return MobileHarvestForm
        return AutocompleteHarvestForm

    def get_success_url(self):
        return reverse('harvestcount.views.garden_details', kwargs={
            'id': self.garden.id,
            'year': self.year,
        })

    def form_invalid(self, form):
        try:
            self.variety = Variety.objects.get(id=form.data['variety'])
        except Exception:
            pass
        return super(HarvestAddView, self).form_invalid(form)

class GardenerAddView(LoginRequiredMixin, PermissionRequiredMixin,
                      RedirectToPreviousPageMixin, CreateView):
    form_class = GardenerForm
    permission = 'harvestcount.add_gardener'
    query_string_exclude = ('gardener',)
    template_name = 'harvestcount/gardeners/add.html'

    def get_initial(self):
        return {
            'garden': Garden.objects.get(id=self.kwargs['id']),
        }

    def get_success_querystring(self):
        return 'gardener=%d' % self.object.pk
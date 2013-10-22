from datetime import date
import json

import unicodecsv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView, FormMixin

from barn.mobile import is_mobile
from farmingconcrete.decorators import in_section, year_in_session
from farmingconcrete.models import Garden, Variety
from farmingconcrete.utils import garden_type_label
from farmingconcrete.views import FarmingConcreteYearMixin
from generic.views import (InitializeUsingGetMixin, LoginRequiredMixin,
                           PermissionRequiredMixin, RedirectToPreviousPageMixin,
                           TitledPageMixin)
from ..views import (AllGardensView, GardenView, IndexView, MetricMixin,
                     RecordsMixin, UserGardenView)
from .forms import GardenerForm, HarvestForm
from .models import Gardener, Harvest


def _harvests(year=settings.FARMINGCONCRETE_YEAR):
    """Get current harvests"""
    return Harvest.objects.filter(recorded__year=year)


class HarvestcountMixin(MetricMixin):

    def get_metric_name(self):
        return 'Harvest Count'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class HarvestcountIndex(HarvestcountMixin, IndexView):
    metric_model = Harvest

    def get_context_data(self, **kwargs):
        context = super(HarvestcountIndex, self).get_context_data(**kwargs)
        harvests = self.get_records()

        gardeners = Gardener.objects.filter(harvest__in=harvests).distinct()
        gardens = Garden.objects.filter(gardener__in=gardeners).distinct()

        context.update({
            'gardens': gardens.count(),
            'gardeners': gardeners.count(),
            'weight': harvests.aggregate(t=Sum('weight'))['t'],
            'plant_types': harvests.values('variety__id').distinct().count(),
            'recent_harvests': harvests.order_by('-added')[:3],
        })

        return context


class GardenDetails(HarvestcountMixin, FormMixin, GardenView):
    form_class = HarvestForm
    metric_model = Harvest

    def get_initial(self):
        garden = self.get_object()

        try:
            most_recent_harvest = Harvest.objects.filter(
                gardener__garden=garden,
                added__year=self.get_year(),
            ).order_by('-added')[0]
            recorded = most_recent_harvest.recorded
            gardener_id = most_recent_harvest.gardener.id
        except:
            recorded = date.today()
            gardener_id = None

        initial = super(GardenDetails, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'garden': garden,
            'gardener': gardener_id,
            'recorded': recorded,
        })
        return initial

    def get_context_data(self, **kwargs):
        garden = self.get_object()
        harvests = self.get_records()

        context = super(GardenDetails, self).get_context_data(**kwargs)
        context.update({
            'form': self.get_form(self.form_class),
            'garden': garden,
            'harvests': harvests.order_by('recorded', 'gardener__name'),
            'plant_types': harvests.values('variety__id').distinct().count(),
            'plants': None,
            'weight': harvests.aggregate(t=Sum('weight'))['t'],
        })
        return context


class HarvestcountUserGardenView(TitledPageMixin, HarvestcountMixin,
                                 UserGardenView):
    metric_model = Harvest

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class HarvestcountAllGardensView(RecordsMixin, TitledPageMixin,
                                 FarmingConcreteYearMixin, HarvestcountMixin,
                                 AllGardensView):
    metric_model = Harvest

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'All counted %s gardens' % garden_type_label(garden_type)


@login_required
@in_section('harvestcount')
@year_in_session
def delete_harvest(request, id, year=None):
    harvest = get_object_or_404(Harvest, pk=id)
    garden_id = harvest.gardener.garden.id
    harvest.delete()
    return redirect('harvestcount_garden_details', pk=garden_id, year=year)


@login_required
@year_in_session
def quantity_for_last_harvest(request, pk=None, year=None):
    garden = pk
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
            harvest = Harvest.objects.filter(
                gardener__garden=garden,
                gardener__pk=gardener,
                variety__pk=variety
            ).order_by('-recorded')[0]
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
    filename = '%s Harvest Count (%s).csv' % (garden.name,
                                              date.today().strftime('%m-%d-%Y'))

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['gardener', 'plant type', 'pounds', 'number of plants',
                     'area (square feet)', 'date'])

    harvests = _harvests(year=year).filter(gardener__garden=garden).distinct()
    for harvest in harvests.order_by('gardener__name', 'variety__name'):
        writer.writerow([
            harvest.gardener.name,
            harvest.variety.name,
            harvest.weight,
            harvest.plants or '',
            harvest.area or '',
            harvest.recorded.strftime('%m-%d-%Y')
        ])

    return response


class HarvestAddView(LoginRequiredMixin, InitializeUsingGetMixin, CreateView):
    form_class = HarvestForm
    template_name = 'metrics/harvestcount/harvests/add.html'

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
        recorded = date.today()
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
                recorded = most_recent_harvest.recorded
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
            'recorded': recorded,
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

    def get_success_url(self):
        kwargs = { 'pk': self.garden.pk, }
        if self.year:
            kwargs['year'] = self.year
        return reverse('harvestcount_garden_details', kwargs=kwargs)

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
    template_name = 'metrics/harvestcount/gardeners/add.html'

    def get_initial(self):
        return {
            'garden': Garden.objects.get(id=self.kwargs['id']),
        }

    def get_success_querystring(self):
        return 'gardener=%d' % self.object.pk


class CreateGardenerView(LoginRequiredMixin, PermissionRequiredMixin,
                         CreateView):
    form_class = GardenerForm
    model = Gardener
    permission = 'harvestcount.add_gardener'
    template_name = 'metrics/harvestcount/gardeners/gardener_form.html'

    def get_existing_gardener(self, garden, name):
        try:
            return self.model.objects.get(garden=garden, name=name)
        except Exception:
            return None

    def form_valid(self, form):
        # Check for gardener with the given name, first
        gardener = self.get_existing_gardener(form.cleaned_data['garden'],
                                              form.cleaned_data['name'])
        if not gardener:
            gardener = self.object = form.save()
        return HttpResponse(json.dumps({
            'name': gardener.name,
            'pk': gardener.pk,
        }), content_type='application/json')

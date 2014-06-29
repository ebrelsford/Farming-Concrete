from datetime import date
import json

import unicodecsv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView

from accounts.utils import get_profile
from farmingconcrete.decorators import in_section, year_in_session
from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from farmingconcrete.views import FarmingConcreteYearMixin
from generic.views import (LoginRequiredMixin, PermissionRequiredMixin,
                           RedirectToPreviousPageMixin, TitledPageMixin)
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin, UserGardenView)
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
            'plant_types': harvests.values('crop__id').distinct().count(),
            'recent_harvests': harvests.order_by('-added')[:3],
        })

        return context


class GardenDetails(HarvestcountMixin, GardenDetailAddRecordView):
    form_class = HarvestForm
    metric_model = Harvest
    template_name = 'metrics/harvestcount/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added harvest to %s' % self.object

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
            'plant_types': harvests.values('crop__id').distinct().count(),
            'plants': None,
            'records': harvests.order_by('recorded', 'gardener__name'),
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
    crop = request.GET.get('crop', None)

    result = {
        'plants': '',
        'area': '',
    }
    if garden and gardener and crop:
        garden = get_object_or_404(Garden, pk=garden)
        if not request.user.has_perm('can_edit_any_garden'):
            profile = get_profile(request.user)
            if garden not in profile.gardens.all():
                return HttpResponseForbidden()
        try:
            harvest = Harvest.objects.filter(
                gardener__garden=garden,
                gardener__pk=gardener,
                crop__pk=crop
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
def download_garden_harvestcount_as_csv(request, pk=None, year=None):
    # TODO move to MetricGardenCSVView
    garden = get_object_or_404(Garden, id=pk)
    filename = '%s Harvest Count (%s).csv' % (garden.name,
                                              date.today().strftime('%m-%d-%Y'))

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['gardener', 'plant type', 'pounds', 'number of plants',
                     'area (square feet)', 'date'])

    harvests = _harvests(year=year).filter(gardener__garden=garden).distinct()
    for harvest in harvests.order_by('gardener__name', 'crop__name'):
        writer.writerow([
            harvest.gardener.name,
            harvest.crop.name,
            harvest.weight,
            harvest.plants or '',
            harvest.area or '',
            harvest.recorded.strftime('%m-%d-%Y')
        ])

    return response


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

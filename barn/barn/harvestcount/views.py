from datetime import date
import json

import unicodecsv

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from farmingconcrete.decorators import garden_type_aware, in_section
from farmingconcrete.models import Garden
from farmingconcrete.forms import GardenForm, FindGardenForm
from models import Gardener, Harvest
from forms import HarvestForm

from middleware.http import Http403

@login_required
@garden_type_aware
@in_section('harvestcount')
def index(request):
    type = request.session['garden_type']

    gardens = Garden.objects.exclude(gardener__harvest=None)
    if type != 'all':
        gardens = gardens.filter(type=type)

    gardeners = Gardener.objects.filter(garden__in=gardens)
    harvests = Harvest.objects.filter(gardener__in=gardeners)

    return render_to_response('harvestcount/index.html', {
        'gardens': gardens.distinct().count(),
        'gardeners': gardeners.distinct().count(),
        'weight': harvests.aggregate(t=Sum('weight'))['t'],
        'plant_types': harvests.values('variety__id').distinct().count(),
        'recent_harvests': harvests.order_by('-added')[:3],
    }, context_instance=RequestContext(request))

@login_required
@garden_type_aware
@in_section('harvestcount')
def add_garden(request):
    if request.method == 'POST':
        form = GardenForm(request.POST, user=request.user)
        if form.is_valid():
            garden = form.save()
            return redirect(garden_details, garden.id)

        find_garden_form = FindGardenForm(request.POST)
        if find_garden_form.is_valid():
            garden = find_garden_form.cleaned_data['garden']
            return redirect(garden_details, garden.id)
    else:
        form = GardenForm(user=request.user)
        find_garden_form = FindGardenForm(user=request.user)

    return render_to_response('harvestcount/gardens/add.html', {
        'form': form,
        'find_garden_form': find_garden_form,
    }, context_instance=RequestContext(request))

@login_required
@in_section('harvestcount')
def garden_details(request, id):
    """Show details for a garden, let user add harvests"""

    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    if request.method == 'POST':
        form = HarvestForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(garden_details, id)
    else:
        try:
            most_recent_harvest = Harvest.objects.filter(gardener__garden=garden).order_by('-added')[0]
            harvested = most_recent_harvest.harvested
            gardener_id = most_recent_harvest.gardener.id
        except:
            harvested = date.today()
            gardener_id = None

        form = HarvestForm(initial={
            'garden': garden,
            'harvested': harvested,
            'gardener': gardener_id,
        }, user=request.user)

    harvests = Harvest.objects.filter(gardener__garden=garden)
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
def user_gardens(request):
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
def all_gardens(request):
    """Show all harvested gardens"""
    type = request.session['garden_type']

    gardens = Garden.objects.exclude(gardener__harvest=None)
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
def delete_harvest(request, id):
    harvest = get_object_or_404(Harvest, pk=id)
    garden_id = harvest.gardener.garden.id
    harvest.delete()
    return redirect(garden_details, garden_id) 

@login_required
def quantity_for_last_harvest(request, id=None):
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
def download_garden_harvestcount_as_csv(request, id):
    garden = get_object_or_404(Garden, pk=id)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s Harvest Count (%s).csv"' % (garden.name, date.today().strftime('%m-%d-%Y'))

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['gardener', 'plant type', 'pounds', 'number of plants', 'area (square feet)', 'date'])

    for gardener in garden.gardener_set.all():
        for harvest in gardener.harvest_set.all():
            writer.writerow([
                gardener.name,
                harvest.variety.name,
                harvest.weight,
                harvest.plants or '',
                harvest.area or '',
                harvest.harvested.strftime('%m-%d-%Y')
            ])

    return response

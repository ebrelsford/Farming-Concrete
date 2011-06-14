from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from farmingconcrete.decorators import garden_type_aware, in_section
from farmingconcrete.models import Garden
from farmingconcrete.forms import GardenForm, FindGardenForm
from models import Gardener, Harvest
from forms import HarvestForm

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

    if request.method == 'POST':
        form = HarvestForm(request.POST, user=request.user)
        if form.is_valid():
            harvest = form.save()
            return redirect(garden_details, id)
    else:
        form = HarvestForm(initial={ 'garden': garden }, user=request.user)

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

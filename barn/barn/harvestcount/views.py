from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from farmingconcrete.decorators import garden_type_aware
from farmingconcrete.models import Garden
from farmingconcrete.forms import GardenForm, FindGardenForm
from harvestcount.models import Gardener, Harvest, HarvestForm

@login_required
@garden_type_aware
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
def garden_details(request, id):
    """Show details for a garden, let user add harvests"""

    garden = get_object_or_404(Garden, pk=id)

    if request.method == 'POST':
        form = HarvestForm(request.POST)
        if form.is_valid():
            harvest = form.save()
            return redirect(garden_details, id)
    else:
        #form = HarvestForm(initial={ 'garden': garden })
        form = HarvestForm()
        form.fields['gardener'].queryset = Gardener.objects.filter(garden=garden)

    harvests = Harvest.objects.filter(gardener__garden=garden)
    return render_to_response('harvestcount/gardens/detail.html', {
        'garden': garden,
        'harvests': harvests,
        'form': form,
        'weight': harvests.aggregate(t=Sum('weight'))['t'],
        'plant_types': harvests.values('variety__id').distinct().count(),
        'plants': None,
    }, context_instance=RequestContext(request))

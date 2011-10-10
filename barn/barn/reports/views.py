from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from cropcount.models import Patch
from farmingconcrete.models import Garden
from harvestcount.models import Harvest
from reports.chart_builders import create_chart_as_png_str

@login_required
def garden_report(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    beds = garden.box_set.all()
    patches = Patch.objects.filter(box__garden=garden)
    harvests = Harvest.objects.filter(gardener__garden=garden)
    return render_to_response('reports/garden.html', {
        'garden': garden,
        'beds': sorted(beds),
        'total_beds': beds.count(),
        'total_area': sum([b.length * b.width for b in beds]),
        'total_plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'crops': patches.values('variety__name').annotate(plants=Sum('plants'), area=Sum('area')),
        'harvests': harvests,
        'harvest_totals': harvests.values('variety__name').annotate(weight=Sum('weight')),
        'gardener_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
        'total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
    }, context_instance=RequestContext(request))

@login_required
def bar_chart_plants_per_crop(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    patches = Patch.objects.filter(box__garden=garden).exclude(plants=None)
    crops = patches.values('variety__name').annotate(plants=Sum('plants'))

    data = {
        'data': [[c['plants'] for c in crops]],
    }
    labels = {
        'x': '',
        'y': 'number of plants',
        'title': '',
    }

    img_str = create_chart_as_png_str('barchart', data, labels, '', xlabels=[c['variety__name'] for c in crops])
    response = HttpResponse(img_str, 'image/png')
    return response

@login_required
def bar_chart_weight_per_crop(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    harvests = Harvest.objects.filter(gardener__garden=garden).exclude(weight=None)
    harvest_totals = harvests.values('variety__name').annotate(weight=Sum('weight'))

    data = {
        'data': [[h['weight'] for h in harvest_totals]],
    }
    labels = {
        'x': '',
        'y': 'total weight measured (lbs)',
        'title': '',
    }

    img_str = create_chart_as_png_str('barchart', data, labels, '', xlabels=[h['variety__name'] for h in harvest_totals])
    response = HttpResponse(img_str, 'image/png')
    return response

@login_required
def bar_chart_weight_per_gardener(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    harvests = Harvest.objects.filter(gardener__garden=garden).exclude(weight=None)
    gardener_totals = harvests.values('gardener__name').annotate(weight=Sum('weight'))

    data = {
        'data': [[g['weight'] for g in gardener_totals]],
    }
    labels = {
        'x': '',
        'y': 'total weight measured (lbs)',
        'title': '',
    }

    img_str = create_chart_as_png_str('barchart', data, labels, '', xlabels=[g['gardener__name'] for g in gardener_totals])
    response = HttpResponse(img_str, 'image/png')
    return response

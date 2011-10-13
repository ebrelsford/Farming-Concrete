from datetime import date
import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from cropcount.models import Patch
from farmingconcrete.models import Garden
from harvestcount.models import Harvest
from chart_builders import create_chart_as_png_str
from models import SharedReport

# TODO parameterize
REPORT_START = date(2011, 01, 01)
REPORT_END = date(2012, 01, 01)

@login_required
def garden_report(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    beds = garden.box_set.all()
    patches = Patch.objects.filter(box__garden=garden, added__gte=REPORT_START, added__lt=REPORT_END)
    harvests = Harvest.objects.filter(gardener__garden=garden, harvested__gte=REPORT_START, harvested__lt=REPORT_END)
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

def shared_garden_report(request, access_key=None):
    shared = get_object_or_404(SharedReport, access_key=access_key)
    return garden_report(request, id=shared.garden.id)

@login_required
def bar_chart_plants_per_crop(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    patches = Patch.objects.filter(box__garden=garden, added__gte=REPORT_START, added__lt=REPORT_END).exclude(plants=None)
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
    harvests = Harvest.objects.filter(gardener__garden=garden, harvested__gte=REPORT_START, harvested__lt=REPORT_END).exclude(weight=None)
    harvest_totals = harvests.values('variety__name').annotate(weight=Sum('weight')).order_by('variety__name')

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
    harvests = Harvest.objects.filter(gardener__garden=garden, harvested__gte=REPORT_START, harvested__lt=REPORT_END).exclude(weight=None)
    gardener_totals = harvests.values('gardener__name').annotate(weight=Sum('weight')).order_by('gardener__name')

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

@login_required
def share(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    shared = SharedReport(garden=garden)
    shared.save()
    results = {
        'url': request.build_absolute_uri(reverse(shared_garden_report, kwargs=dict(access_key=shared.access_key))),
    }
    return HttpResponse(json.dumps(results), mimetype='application/json')


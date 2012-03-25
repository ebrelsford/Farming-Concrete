import json
from StringIO import StringIO

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django_xhtml2pdf.utils import render_to_pdf_response

from charts import plants_per_crop, weight_per_crop, weight_per_gardener, estimated_weight_per_crop
from cropcount.models import Box, Patch
from estimates.common import estimate_for_harvests_by_gardener, estimate_for_patches
from farmingconcrete.models import Garden, GardenType
from harvestcount.models import Harvest
from models import SharedReport, Chart

def _harvests(garden=None, borough=None, type=None, year=2011): # TODO un-hard-code
    """Get valid harvests for the given garden"""
    harvests = Harvest.objects.filter(harvested__year=year)
    if garden:
        return harvests.filter(gardener__garden=garden)
    if borough:
        harvests = harvests.filter(gardener__garden__borough=borough)
    if type:
        harvests = harvests.filter(gardener__garden__type__name=type)

    return harvests.distinct()

def _patches(garden=None, borough=None, type=None, year=2011): # TODO un-hard-code
    """Get valid patches for the given garden"""
    patches = Patch.objects.filter(added__year=year)
    if garden:
        return patches.filter(box__garden=garden)
    if borough:
        patches = patches.filter(box__garden__borough=borough)
    if type:
        patches = patches.filter(box__garden__type__name=type)
    
    return patches.distinct()

def _boroughs(year):
    cropcount_gardens = Garden.objects.filter(box__patch__added__year=year)
    harvestcount_gardens = Garden.objects.filter(gardener__harvest__harvested__year=year)
    return (cropcount_gardens | harvestcount_gardens).values_list('borough', flat=True).order_by('borough').distinct()

def _report_common_context(borough=None, garden=None, type=None, year=None):
    patches = _patches(borough=borough, garden=garden, type=type, year=year).distinct()
    harvests = _harvests(borough=borough, garden=garden, type=type, year=year)
    beds = Box.objects.filter(patch__in=patches).distinct()
    estimated_yield = estimate_for_patches(patches, estimate_yield=True, estimate_value=True, garden_type=type)

    return {
        'beds': sorted(beds),
        'total_beds': beds.count(),
        'total_area': sum([b.length * b.width for b in beds]),
        'total_plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'crops': estimated_yield['crops'],
        'total_estimated_yield': estimated_yield['total_yield'],
        'total_estimated_yield_type': estimated_yield['total_yield_by_garden_type'],
        'total_estimated_value': estimated_yield['total_value'],
        'total_estimated_value_type': estimated_yield['total_value_by_garden_type'],

        'harvests': harvests,
        'harvest_totals': harvests.values('variety__name').annotate(weight=Sum('weight')),
        'harvestcount_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
        'total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
    }

@login_required
def index(request, year=2011): # TODO un-hard-code
    borough = request.GET.get('borough', None)
    type = request.GET.get('type', None)
    if type:
        type = GardenType.objects.get(short_name=type);

    context = _report_common_context(borough=borough, type=type, year=year)
    cropcount_gardens = Garden.objects.filter(box__patch__added__year=year)
    harvestcount_gardens = Garden.objects.filter(gardener__harvest__harvested__year=year)
    if borough:
        cropcount_gardens = cropcount_gardens.filter(borough=borough)
        harvestcount_gardens = harvestcount_gardens.filter(borough=borough)
    if type:
        cropcount_gardens = cropcount_gardens.filter(type=type)
        harvestcount_gardens = harvestcount_gardens.filter(type=type)

    context['cropcount_gardens_count'] = cropcount_gardens.distinct().count()
    context['harvestcount_gardens_count'] = harvestcount_gardens.distinct().count()
    context['boroughs'] = _boroughs(year)
    context['year'] = year
    context['borough'] = borough
    context['type'] = type

    return render_to_response('reports/index.html', context, context_instance=RequestContext(request))

@login_required
def garden_report(request, id=None, year=2011): # TODO un-hard-code?
    return _render_garden_report(request, id=id, year=year)

def shared_garden_report(request, access_key=None):
    shared = get_object_or_404(SharedReport, access_key=access_key)
    return _render_garden_report(request, id=shared.garden.id)

def _render_garden_report(request, id=None, year=None):
    """render the report for a given garden"""
    garden = get_object_or_404(Garden, id=id)
    context = _report_common_context(garden=garden, year=year)
    context['garden'] = garden

    return render_to_response('reports/garden.html', context, context_instance=RequestContext(request))

@login_required
def bar_chart_plants_per_crop(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    response = HttpResponse(plants_per_crop(garden), 'image/png')
    return response

@login_required
def bar_chart_weight_per_crop(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    response = HttpResponse(weight_per_crop(garden), 'image/png')
    return response

@login_required
def bar_chart_weight_per_gardener(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    response = HttpResponse(weight_per_gardener(garden), 'image/png')
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

@login_required
def pdf(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    harvests = _harvests(garden)
    patches = _patches(garden)

    cropcount_estimates = estimate_for_patches(patches, estimate_yield=True, estimate_value=True)
    harvestcount_estimates = estimate_for_harvests_by_gardener(harvests, estimate_value=True)
    harvestcount_totals = harvests.values('gardener__name').annotate(weight=Sum('weight'))
    for row in harvestcount_totals:
        row['value'] = harvestcount_estimates['gardener_values'][row['gardener__name']]

    charts = _make_charts(garden, medium='print')
    for key, c in charts.items():
        print c.image.url

    return render_to_pdf_response('reports/pdf.html', context=RequestContext(request, {
        'garden': garden,
        'has_harvestcount': harvests.count() > 0,       
        'has_cropcount': patches.count() > 0,       

        'charts': charts,

        'harvestcount_total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
        'harvestcount_estimated_total_value': harvestcount_estimates['total_value'],
        'harvestcount_totals': harvestcount_totals,

        'cropcount_estimated_pounds': cropcount_estimates['total_yield'],
        'cropcount_estimated_value': cropcount_estimates['total_value'],
    }), pdfname='report.pdf')

@login_required
def pdftest(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    harvests = _harvests(garden)

    return render_to_response('reports/pdf.html', RequestContext(request, {
        'garden': garden,
        'charts': _make_charts(garden),
        'harvestcount_total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
        'harvestcount_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
    }))

def _make_charts(garden, medium="screen"):
    charts = {}

    chart_functions = [weight_per_crop, estimated_weight_per_crop]

    for f in chart_functions:
        try:
            label = f.__name__
            c = Chart(garden=garden, label=label)
            temp_file = File(StringIO(f(garden, medium=medium)))
            c.image.save('%d_%s_%s.png' % (garden.id, label, medium), ContentFile(temp_file.read()), save=True)
            charts[label] = c
        except:
            pass

    return charts

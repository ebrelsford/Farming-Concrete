from datetime import date
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

from cropcount.models import Box, Patch
from estimates.models import EstimatedYield
from farmingconcrete.models import Garden
from harvestcount.models import Harvest
from charts import plants_per_crop, weight_per_crop, weight_per_gardener
from models import SharedReport, Chart

# TODO parameterize
REPORT_START = date(2011, 01, 01)
REPORT_END = date(2012, 01, 01)

def _harvests(garden=None, borough=None, start=REPORT_START, end=REPORT_END):
    """Get valid harvests for the given garden"""
    harvests = Harvest.objects.filter(harvested__gte=start, harvested__lt=end)
    if garden:
        return harvests.filter(gardener__garden=garden)
    elif borough:
        return harvests.filter(gardener__garden__borough=borough)

    return harvests

def _patches(garden=None, borough=None, start=REPORT_START, end=REPORT_END):
    """Get valid patches for the given garden"""
    patches = Patch.objects.filter(added__gte=start, added__lt=end)
    if garden:
        return patches.filter(box__garden=garden)
    elif borough:
        return patches.filter(box__garden__borough=borough)
    
    return patches

def _report_common_context(borough=None, garden=None):
    if borough:
        patches = _patches(borough=borough).distinct()
        harvests = _harvests(borough=borough)
    elif garden:
        patches = _patches(garden=garden)
        harvests = _harvests(garden=garden)
    else:
        patches = _patches().distinct()
        harvests = _harvests()

    beds = Box.objects.filter(patch__in=patches).distinct()

    # TODO estimates for crops that weren't weighed + actual weights for those which were?
    crops = patches.values('variety__id', 'variety__name').annotate(plants=Sum('plants'), area=Sum('area')).distinct()
    for crop in crops:
        # XXX should use 'added' to get more granular estimated yield
        crop['estimate'] = _estimate_yield(crop['variety__id'], date(2011, 6, 1), crop['plants'])

    return {
        'beds': sorted(beds),
        'total_beds': beds.count(),
        'total_area': sum([b.length * b.width for b in beds]),
        'total_plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'crops': crops,

        'harvests': harvests,
        'harvest_totals': harvests.values('variety__name').annotate(weight=Sum('weight')),
        'gardener_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
        'total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
    }

@login_required
def index(request):
    context = _report_common_context()
    year = request.session['year']
    cropcount_gardens = Garden.objects.filter(box__patch__added__year=year)
    harvestcount_gardens = Garden.objects.filter(gardener__harvest__harvested__year=year)
    context['cropcount_gardens_count'] = cropcount_gardens.distinct().count()
    context['harvestcount_gardens_count'] = harvestcount_gardens.distinct().count()
    context['boroughs'] = (cropcount_gardens | harvestcount_gardens).values_list('borough', flat=True).order_by('borough').distinct()

    return render_to_response('reports/index.html', context, context_instance=RequestContext(request))

@login_required
def borough_report(request, borough=None):
    context = _report_common_context(borough=borough)
    context['borough'] = borough

    year = request.session['year']
    cropcount_gardens = Garden.objects.filter(borough=borough, box__patch__added__year=year)
    harvestcount_gardens = Garden.objects.filter(borough=borough, gardener__harvest__harvested__year=year)
    context['cropcount_gardens_count'] = cropcount_gardens.distinct().count()
    context['harvestcount_gardens_count'] = harvestcount_gardens.distinct().count()

    return render_to_response('reports/borough.html', context, context_instance=RequestContext(request))

@login_required
def garden_report(request, id=None):
    return _render_garden_report(request, id=id)

def shared_garden_report(request, access_key=None):
    shared = get_object_or_404(SharedReport, access_key=access_key)
    return _render_garden_report(request, id=shared.garden.id)

def _estimate_yield(variety_id, recorded_date, plants):
    estimates = EstimatedYield.objects.filter(variety__id=variety_id, valid_start__lte=recorded_date, valid_end__gt=recorded_date, should_be_used=True)
    try:
        return estimates[0].pounds_per_plant * plants
    except:
        return None

def _render_garden_report(request, id=None):
    """render the report for a given garden"""
    garden = get_object_or_404(Garden, id=id)
    context = _report_common_context(garden=garden)
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

    return render_to_pdf_response('reports/pdf.html', context=RequestContext(request, {
        'garden': garden,
        'charts': _make_charts(garden),
        'total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
        'gardener_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
    }), pdfname='report.pdf')

@login_required
def pdftest(request, id=None):
    garden = get_object_or_404(Garden, id=id)
    harvests = _harvests(garden)

    return render_to_response('reports/pdf.html', RequestContext(request, {
        'garden': garden,
        'charts': _make_charts(garden),
        'total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
        'gardener_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
    }))

def _make_charts(garden):
    charts = {}

    chart_functions = [plants_per_crop, weight_per_crop, weight_per_gardener,]

    for f in chart_functions:
        try:
            label = f.__name__
            c = Chart(garden=garden, label=label)
            temp_file = File(StringIO(f(garden)))
            c.image.save('%d_%s.png' % (garden.id, label), ContentFile(temp_file.read()), save=True)
            charts[label] = c
        except:
            pass

    return charts

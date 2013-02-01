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

from charts import (plants_per_crop, weight_per_crop, weight_per_gardener,
        estimated_weight_per_crop)
from cropcount.models import Box
from estimates.common import (estimate_for_harvests_by_gardener_and_variety,
        estimate_for_patches)
from farmingconcrete.models import Garden, GardenType
from common import (filter_harvests, filter_patches, filter_boroughs,
        consolidate_totals, get_garden_counts_by_type)
from models import SharedReport, Chart
from settings import FARMINGCONCRETE_YEAR


@login_required
def index(request, year=FARMINGCONCRETE_YEAR):
    borough = request.GET.get('borough', None)
    type = request.GET.get('type', None)
    use_all_cropcount = request.GET.get('use_all_cropcount', False)

    if type:
        type = GardenType.objects.get(short_name=type);

    context = _context(borough=borough, type=type, year=year, use_all_cropcount=use_all_cropcount)

    cropcount_gardens = Garden.objects.filter(box__in=context['beds']) # TODO likely slow, should move to wherever filtering happens (eg, filter_patches())
    harvestcount_gardens = Garden.objects.filter(gardener__harvest__harvested__year=year)
    if borough:
        cropcount_gardens = cropcount_gardens.filter(borough=borough)
        harvestcount_gardens = harvestcount_gardens.filter(borough=borough)
    if type:
        cropcount_gardens = cropcount_gardens.filter(type=type)
        harvestcount_gardens = harvestcount_gardens.filter(type=type)

    context.update({
        'cropcount_gardens_count': cropcount_gardens.distinct().count(),
        'harvestcount_gardens_count': harvestcount_gardens.distinct().count(),
        'boroughs': filter_boroughs(year),
        'year': year,
        'borough': borough,
        'type': type,
        'use_all_cropcount': use_all_cropcount,
    })

    return render_to_response('reports/index.html', context, context_instance=RequestContext(request))


@login_required
def garden_report(request, id=None, year=FARMINGCONCRETE_YEAR):
    """get the report for the garden"""
    return _render_garden_report(request, id=id, year=year)


def _render_garden_report(request, id=None, year=None):
    """render the report for a given garden"""
    garden = get_object_or_404(Garden, id=id)
    context = _context(garden=garden, year=year)
    return render_to_response('reports/garden.html', context, context_instance=RequestContext(request))


def shared_garden_report(request, access_key=None):
    """allow access to a garden's report for someone with whom it was shared"""
    shared = get_object_or_404(SharedReport, access_key=access_key)
    return _render_garden_report(request, id=shared.garden.id, year=shared.valid_year)


@login_required
def share(request, id=None, year=None):
    garden = get_object_or_404(Garden, id=id)
    shared = SharedReport(garden=garden, valid_year=year)
    shared.save()
    results = {
        'url': request.build_absolute_uri(reverse(shared_garden_report, kwargs=dict(access_key=shared.access_key))),
    }
    return HttpResponse(json.dumps(results), mimetype='application/json')


@login_required
def pdf(request, id=None, year=None):
    garden = get_object_or_404(Garden, id=id)

    context = _context(garden=garden, year=year)
    context['charts'] = _make_charts(garden, year=year, medium='print')
    context['garden_name_length'] = len(garden.name)
    return render_to_pdf_response('reports/pdf.html', context=RequestContext(request, context), pdfname='report.pdf')



#
# common data-loading/filtering methods
#


def _context(borough=None, garden=None, type=None, year=None, use_all_cropcount=False):
    """get the common context for all reports"""
    patches = filter_patches(borough=borough, garden=garden, type=type, year=year, use_all_cropcount=use_all_cropcount).distinct()
    harvests = filter_harvests(borough=borough, garden=garden, type=type, year=year)
    beds = Box.objects.filter(patch__in=patches).distinct()
    estimated_yield = estimate_for_patches(patches, estimate_yield=True, estimate_value=True, garden_type=type)
    harvestcount_estimates = estimate_for_harvests_by_gardener_and_variety(harvests)

    context = {
        'year': year,

        'beds': sorted(beds),
        'total_beds': beds.count(),
        'total_area': sum([b.length * b.width for b in beds]),
        'total_plants': patches.aggregate(Sum('plants'))['plants__sum'],

        'crops': estimated_yield['crops'],
        'total_estimated_yield': estimated_yield['total_yield'],
        'total_estimated_yield_type': estimated_yield['total_yield_by_garden_type'],
        'total_estimated_value': estimated_yield['total_value'],
        'total_estimated_value_type': estimated_yield['total_value_by_garden_type'],
        'variety_totals': estimated_yield['variety_totals'],
        'total_plants_with_yields': estimated_yield['total_plants_with_yields'],

        'harvests': harvests,
        'harvest_totals': harvests.values('variety__name').annotate(weight=Sum('weight')),
        'harvestcount_totals': harvests.values('gardener__name').annotate(weight=Sum('weight')),
        'harvestcount_total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
        'harvestcount_estimated_total_value': harvestcount_estimates['total_value'],
        'harvestcount_gardener_totals': [(k, harvestcount_estimates['gardener_totals'][k]) for k in sorted(harvestcount_estimates['gardener_totals'])],
        'harvestcount_crop_totals': [(k, harvestcount_estimates['crop_totals'][k]) for k in sorted(harvestcount_estimates['crop_totals'])],
        'total_weight': harvests.aggregate(Sum('weight'))['weight__sum'],
    }
    if garden:
        context.update({
            'garden': garden,
            'has_harvestcount': harvests.count() > 0,
            'has_cropcount': patches.count() > 0,
        })
    else:
        garden_harvest_totals = harvestcount_estimates['garden_totals']
        garden_crop_totals = estimated_yield['garden_totals']
        context.update(
            consolidate_totals(garden_harvest_totals, garden_crop_totals)
        )
        context['garden_counts'] = get_garden_counts_by_type(garden_harvest_totals, garden_crop_totals)
    return context



#
# charts
#


@login_required
def bar_chart_plants_per_crop(request, id=None, year=None):
    garden = get_object_or_404(Garden, id=id)
    response = HttpResponse(plants_per_crop(garden, year=year), 'image/png')
    return response


@login_required
def bar_chart_weight_per_crop(request, id=None, year=None):
    garden = get_object_or_404(Garden, id=id)
    response = HttpResponse(weight_per_crop(garden, year=year), 'image/png')
    return response


@login_required
def bar_chart_weight_per_gardener(request, id=None, year=None):
    garden = get_object_or_404(Garden, id=id)
    response = HttpResponse(weight_per_gardener(garden, year=year), 'image/png')
    return response


def _make_charts(garden, year=None, medium="screen"):
    charts = {}

    chart_functions = [weight_per_crop, estimated_weight_per_crop]

    for f in chart_functions:
        try:
            label = f.__name__
            c = Chart(garden=garden, label=label)
            temp_file = File(StringIO(f(garden, year=year, medium=medium)))
            c.image.save('%d_%s_%s.png' % (garden.id, label, medium), ContentFile(temp_file.read()), save=True)
            charts[label] = c
        except:
            pass


    return charts

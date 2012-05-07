import json

from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cropcount.models import Box
from estimates.common import estimate_for_harvests_by_gardener_and_variety, estimate_for_patches
from farmingconcrete.models import Garden
from reports.common import filter_harvests, filter_patches, filter_boroughs, filter_neighborhoods, consolidate_totals, filter_varieties
from settings import FARMINGCONCRETE_YEAR

def map(request):
    context = {
        'year': str(FARMINGCONCRETE_YEAR),
        'varieties': {
            '2010': filter_varieties('2010'),
            '2011': filter_varieties('2011'),
        },
        'neighborhoods': {
            '2010': filter_neighborhoods('2010'),
            '2011': filter_neighborhoods('2011'),
        },
        'boroughs': {
            '2010': filter_boroughs('2010'),
            '2011': filter_boroughs('2011'),
        },
    }
    return render_to_response('harvestmap/map.html', context,
                              context_instance=RequestContext(request))

def kml(request):
    """Get kml for requested gardens for harvest map"""

    year = request.GET.get('year', FARMINGCONCRETE_YEAR)
    context = {
        'gardens': _gardens(year=year)
    }
    return render_to_response('harvestmap/gardens.kml', context,
                              context_instance=RequestContext(request),
                              mimetype='application/vnd.google-earth.kml+xml')

def data(request):
    """
    Get data for the harvest map.
    """
    borough = request.GET.get('borough', 'all')
    neighborhood = request.GET.get('neighborhood', 'all')
    variety = request.GET.get('variety', 'all')
    year = request.GET.get('year', None)

    if borough == 'all': borough = None
    if neighborhood == 'all': neighborhood = None
    if variety == 'all': variety = None

    if year:
        totals = _get_data(year, borough=borough, neighborhood=neighborhood, 
                           variety=variety)
    else:
        totals = {}
    
    return HttpResponse(json.dumps(totals), mimetype='application/json')

def _get_data(year, borough=None, neighborhood=None, variety=None, type=None):
    """
    Get sidebar data for the given parameters.
    """
    patches = filter_patches(borough=borough, neighborhood=neighborhood, 
                             year=year, variety=variety).distinct()
    beds = Box.objects.filter(patch__in=patches).distinct()
    harvests = filter_harvests(borough=borough, neighborhood=neighborhood,
                               type=type, year=year, variety=variety)

    cropcount_estimates = estimate_for_patches(patches, estimate_yield=True,
                                               estimate_value=True,
                                               garden_type=type)
    harvestcount_estimates = estimate_for_harvests_by_gardener_and_variety(harvests)

    garden_harvest_totals = harvestcount_estimates['garden_totals']
    garden_crop_totals = cropcount_estimates['garden_totals']
    overall = consolidate_totals(garden_harvest_totals, garden_crop_totals)

    gardens = harvestcount_estimates['garden_ids'].union(cropcount_estimates['garden_ids'])

    return {
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'pounds': int(round(overall['overall_weight'], -1)), # nearest ten
        'area': float(sum([b.length * b.width for b in beds])),
        'cost': int(round(overall['overall_value'], -1)), # nearest ten
        'gardens': list(gardens),
    }

def _gardens(borough=None, neighborhood=None, variety=None, year=None):
    gardens = Garden.objects.exclude(latitude=None, longitude=None)

    if borough:
        gardens = gardens.filter(borough=borough)
    if borough:
        gardens = gardens.filter(neighborhood=neighborhood)

    if variety:
        gardens = gardens.filter(Q(gardener__harvest__harvested__year=year,
                                   gardener__harvest__variety__name=variety) |
                                 Q(box__patch__added__year=year,
                                   box__patch__variety__name=variety))
    else:
        gardens = gardens.filter(Q(gardener__harvest__harvested__year=year) |
                                 Q(box__patch__added__year=year))

    gardens = gardens.distinct()
    return gardens

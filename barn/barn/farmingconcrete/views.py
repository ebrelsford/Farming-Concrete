from datetime import date
import geojson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from models import Garden, GardenType
from farmingconcrete.geo import garden_collection

# TODO parameterize
PATCH_ADDED_START = date(2011, 01, 01)
PATCH_ADDED_END = date(2012, 01, 01)
HARVESTED_START = date(2011, 01, 01)
HARVESTED_END = date(2012, 01, 01)

def index(request):
    return render_to_response('farmingconcrete/index.html', { }, context_instance=RequestContext(request))

@login_required
def account(request):
    return render_to_response('farmingconcrete/account.html', { }, context_instance=RequestContext(request))

@login_required
def switch_garden_type(request, type='all'):
    next = request.GET['next']
    request.session['garden_type'] = type = _get_garden_type(type)
    return redirect(next)

def gardens_geojson(request):
    """Get GeoJSON for requested gardens"""

    gardens = Garden.objects.exclude(latitude=None, longitude=None)

    ids = request.GET.get('ids', None)
    cropcount = request.GET.get('cropcount', None)
    harvestcount = request.GET.get('harvestcount', None)
    type = request.GET.get('type', None)

    if ids:
        ids = ids.split(',')
        gardens = gardens.filter(id__in=ids)
    if cropcount and cropcount != 'no':
        gardens = gardens.exclude(box=None).filter(box__patch__added__gte=PATCH_ADDED_START, box__patch__added__lt=PATCH_ADDED_END).distinct()
    if harvestcount and harvestcount != 'no':
        gardens = gardens.exclude(gardener__harvest=None).filter(gardener__harvest__harvested__gte=HARVESTED_START, gardener__harvest__harvested__lt=HARVESTED_END).distinct()
    if type and type != 'all':
        gardens = gardens.filter(type__short_name=type)

    return HttpResponse(geojson.dumps(garden_collection(gardens)), mimetype='application/json')

def _get_garden_type(short_name):
    types = GardenType.objects.filter(short_name=short_name)
    if types.count() > 0:
        return types[0]

    return 'all'

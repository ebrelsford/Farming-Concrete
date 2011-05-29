import geojson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from models import Garden, GardenType
from farmingconcrete.geo import garden_collection, garden_feature

@login_required
def account(request):
    return render_to_response('farmingconcrete/account.html', { }, context_instance=RequestContext(request))

@login_required
def switch_garden_type(request, type='all'):
    next = request.GET['next']
    request.session['garden_type'] = type = _get_garden_type(type)
    return redirect(next)

@login_required
def gardens_geojson(request):
    """Get GeoJSON for requested gardens"""

    gardens = Garden.objects.all()

    ids = request.GET.get('ids', None)
    cropcount = request.GET.get('cropcount', None)
    type = request.GET.get('type', None)

    if ids:
        ids = ids.split(',')
        gardens = gardens.filter(id__in=ids)
    if cropcount and cropcount != 'no':
        gardens = gardens.exclude(box=None)
    if type and type != 'all':
        gardens = gardens.filter(type__short_name=type)

    return HttpResponse(geojson.dumps(garden_collection(gardens)), mimetype='application/json')

def _get_garden_type(short_name):
    types = GardenType.objects.filter(short_name=short_name)
    if types.count() > 0:
        return types[0]

    return 'all'

@login_required
def garden_geojson(request, id):
    """Get the geojson for one garden"""

    garden = get_object_or_404(Garden, pk=id)
    return HttpResponse(geojson.dumps(garden_collection([garden,])), mimetype='application/json')

import geojson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect

from models import Garden
from farmingconcrete.geo import garden_collection, garden_feature

@login_required
def account(request):
    return render_to_response('farmingconcrete/account.html', { })

@login_required
def switch_garden_type(request, type='all'):
    next = request.GET['next']
    request.session['garden_type'] = type = _get_garden_type(type)
    return redirect(next)

def _get_garden_type(type):
    if type in map(lambda l: l[0], Garden.TYPE_CHOICES):
        return type
    return 'all'

@login_required
def garden_geojson(request, id):
    """Get the geojson for one garden"""

    garden = get_object_or_404(Garden, pk=id)
    return HttpResponse(geojson.dumps(garden_collection([garden,])), mimetype='application/json')

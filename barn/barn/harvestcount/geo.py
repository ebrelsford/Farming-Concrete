import geojson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from farmingconcrete.decorators import garden_type_aware
from farmingconcrete.geo import *
from farmingconcrete.models import Garden
from harvestcount.models import Gardener, Harvest

@login_required
@garden_type_aware
def harvested_geojson(request):
    """get GeoJSON for Gardens with Harvests"""
    type = request.session['garden_type']
    gardens = Garden.objects.exclude(gardener__harvest=None)
    if type != 'all':
        gardens = gardens.filter(type=type)

    return HttpResponse(geojson.dumps(garden_collection(gardens)), mimetype='application/json')

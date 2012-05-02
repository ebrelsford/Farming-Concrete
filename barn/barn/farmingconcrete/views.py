import geojson
import simplekml

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from middleware.http import Http403
from models import Garden, GardenType
from farmingconcrete.decorators import year_in_session
from farmingconcrete.geo import garden_collection
from cropcount.models import Box, Patch
from harvestcount.models import Harvest

from settings import FARMINGCONCRETE_YEAR

def _harvests(year=FARMINGCONCRETE_YEAR):
    """Get current harvests"""
    return Harvest.objects.filter(harvested__year=year)

def _patches(year=FARMINGCONCRETE_YEAR):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)

@year_in_session
def index(request, year=None):
    user_gardens = []
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        user_gardens = profile.gardens.all().order_by('name')
    return render_to_response('farmingconcrete/index.html', {
        'user_gardens': user_gardens,
    }, context_instance=RequestContext(request))

@login_required
@year_in_session
def garden_details(request, id, year=None):
    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    patches = _patches(year=year).filter(box__garden=garden)
    beds = Box.objects.filter(patch__in=patches).distinct()
    harvests = _harvests(year=year).filter(gardener__garden=garden)

    return render_to_response('farmingconcrete/gardens/detail.html', {
        'garden': garden,
        'beds': beds.count(),
        'area': beds.extra(select = {'total': 'sum(length * width)'})[0].total,
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'harvests': harvests.order_by('harvested', 'gardener__name'),
        'weight': harvests.aggregate(t=Sum('weight'))['t'],
        'plant_types': harvests.values('variety__id').distinct().count(),
    }, context_instance=RequestContext(request))

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
    participating = request.GET.get('participating', None)
    type = request.GET.get('type', None)
    borough = request.GET.get('borough', None)
    year = request.GET.get('year', FARMINGCONCRETE_YEAR)

    if ids:
        ids = ids.split(',')
        gardens = gardens.filter(id__in=ids)
    if type and type != 'all':
        gardens = gardens.filter(type__short_name=type)
    if borough:
        gardens = gardens.filter(borough=borough)

    if cropcount and cropcount != 'no':
        gardens = gardens.filter(box__patch__added__year=year)
    elif harvestcount and harvestcount != 'no':
        gardens = gardens.filter(gardener__harvest__harvested__year=year)
    elif participating and participating != 'no':
        gardens = gardens.filter(Q(box__patch__added__year=year) | 
                                 Q(gardener__harvest__harvested__year=year))

    gardens = gardens.distinct()
    return HttpResponse(geojson.dumps(garden_collection(gardens)), mimetype='application/json')

def gardens_harvest_map_kml(request):
    """Get GeoJSON for requested gardens for harvest map"""

    type = request.GET.get('type', None)
    borough = request.GET.get('borough', None)
    neighborhood = request.GET.get('neighborhood', None)
    year = request.GET.get('year', FARMINGCONCRETE_YEAR)
    variety = request.GET.get('variety', None)

    gardens = _gardens(borough=borough, neighborhood=neighborhood, year=year, 
                       variety=variety)

    kml = simplekml.Kml()
    f = kml.newfolder()
    for g in gardens:
        f.newpoint(name=g.name, coords=[(g.latitude, g.longitude)])
    return HttpResponse(kml.kml(format=False),
                        mimetype='application/vnd.google-earth.kml+xml')

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

def _get_garden_type(short_name):
    types = GardenType.objects.filter(short_name=short_name)
    if types.count() > 0:
        return types[0]

    return 'all'

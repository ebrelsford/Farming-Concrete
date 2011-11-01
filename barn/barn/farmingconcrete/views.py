from datetime import date
import geojson

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from middleware.http import Http403
from models import Garden, GardenType
from farmingconcrete.geo import garden_collection
from cropcount.models import Box, Patch
from harvestcount.models import Harvest

# TODO parameterize
PATCH_ADDED_START = date(2011, 01, 01)
PATCH_ADDED_END = date(2012, 01, 01)
HARVESTED_START = date(2011, 01, 01)
HARVESTED_END = date(2012, 01, 01)

def _harvests(start=HARVESTED_START, end=HARVESTED_END):
    """Get current harvests"""
    return Harvest.objects.filter(harvested__gte=start, harvested__lt=end)

def _patches(start=PATCH_ADDED_START, end=PATCH_ADDED_END):
    """Get current patches"""
    return Patch.objects.filter(added__gte=start, added__lt=end)

def index(request):
    user_gardens = []
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        user_gardens = profile.gardens.all().order_by('name')
    return render_to_response('farmingconcrete/index.html', {
        'user_gardens': user_gardens,
    }, context_instance=RequestContext(request))

@login_required
def garden_details(request, id):
    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    patches = _patches().filter(box__garden=garden)
    beds = Box.objects.filter(patch__in=patches).distinct()
    harvests = _harvests().filter(gardener__garden=garden)

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

    if ids:
        ids = ids.split(',')
        gardens = gardens.filter(id__in=ids)
    if cropcount and cropcount != 'no':
        gardens = gardens.filter(box__patch__added__year=CURRENT_YEAR)
    if harvestcount and harvestcount != 'no':
        gardens = gardens.filter(gardener__harvest__harvested__year=CURRENT_YEAR)
    if participating and participating != 'no':
        gardens = gardens.filter(box__patch__added__year=CURRENT_YEAR) | gardens.filter(gardener__harvest__harvested__year=CURRENT_YEAR)
    if type and type != 'all':
        gardens = gardens.filter(type__short_name=type)

    gardens = gardens.distinct()
    return HttpResponse(geojson.dumps(garden_collection(gardens)), mimetype='application/json')

def _get_garden_type(short_name):
    types = GardenType.objects.filter(short_name=short_name)
    if types.count() > 0:
        return types[0]

    return 'all'

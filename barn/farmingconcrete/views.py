import geojson
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.base import View
from django.views.generic.list import ListView

from cropcount.models import Box, Patch
from farmingconcrete.decorators import year_in_session
from farmingconcrete.geo import garden_collection
from farmingconcrete.models import Garden, GardenType, Variety
from farmingconcrete.utils import get_variety
from generic.views import LoginRequiredMixin, PermissionRequiredMixin, RememberPreviousPageMixin
from harvestcount.models import Harvest
from middleware.http import Http403

def _harvests(year=settings.FARMINGCONCRETE_YEAR):
    """Get current harvests"""
    return Harvest.objects.filter(harvested__year=year)

def _patches(year=settings.FARMINGCONCRETE_YEAR):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)

@year_in_session
def index(request, year=settings.FARMINGCONCRETE_YEAR):
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
    year = request.GET.get('year', settings.FARMINGCONCRETE_YEAR)

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

def _get_garden_type(short_name):
    types = GardenType.objects.filter(short_name=short_name)
    if types.count() > 0:
        return types[0]

    return 'all'

class GardenListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Garden.objects.all().order_by('name')

class UserGardensListView(LoginRequiredMixin, ListView):
    template_name='farmingconcrete/user_garden_list.html'

    def get_queryset(self):
        return self.request.user.get_profile().gardens.all()

class VarietyPickerListView(LoginRequiredMixin, RememberPreviousPageMixin, ListView):
    query_string_exclude = ('variety', 'variety_text')

    def get_queryset(self):
        return (Variety.objects.filter(needs_moderation=False) |
                self.request.user.farmingconcrete_variety_added.all())

class VarietyAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    http_method_names = ['post',]
    permission = 'farmingconcrete.add_variety'

    def variety_exists(self, name):
        return Variety.objects.filter(name=name).count() > 0

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        force = request.POST.get('force', False) == 'true'
        variety = None

        if self.variety_exists(name) or force:
            # create the variety no matter what
            variety, created = get_variety(name, request.user)

        if not variety:
            # either variety-creating failed...
            message = 'failed to create new plant type'
            if not force:
                # ...or we were not allowed to force it
                message = 'not found'

            return HttpResponse(json.dumps({
                'success': False,
                'id': None,
                'name': None,
                'message': message,
            }))

        message = 'plant type %s added' % variety.name
        if not created:
            message = 'looks good! found %s.' % variety.name

        return HttpResponse(json.dumps({
            'success': True,
            'id': variety.id,
            'name': variety.name,
            'message': message,
        }))

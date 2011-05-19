import geojson

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

from ajax_select import make_ajax_form

from farmingconcrete.models import Garden
from farmingconcrete.forms import GardenForm
from farmingconcrete.geo import garden_collection
from farmingconcrete.decorators import garden_type_aware, in_section
from cropcount.models import Box, Patch
from cropcount.forms import UncountedGardenForm, BoxForm, PatchForm

from middleware.http import Http403

@login_required
@garden_type_aware
@in_section('cropcount')
def index(request):
    """Home page for Crop Count. Show current stats, give access to next actions."""
    type = request.session['garden_type']

    counted_gardens = Garden.objects.exclude(box=None)
    beds = Box.objects.all()
    patches = Patch.objects.all()

    # filter more if we need to
    if type != 'all':
        counted_gardens = counted_gardens.filter(type=type)
        beds = beds.filter(garden__type=type)
        patches = patches.filter(box__garden__type=type)
    
    return render_to_response('cropcount/index.html', {
        'gardens': counted_gardens.count(),
        'area': beds.extra(select = {'total': 'sum(length * width)'})[0].total,
        'beds': beds.count(),
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'recent_types': patches.order_by('-added')[:3],
        'type': type,
    }, context_instance=RequestContext(request))

@login_required
@garden_type_aware
@in_section('cropcount')
def gardens(request):
    """Show counted gardens, let user add more"""

    type = request.session['garden_type']

    counted_gardens = Garden.counted()
    if type != 'all':
        counted_gardens = counted_gardens.filter(type=type)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        counted_gardens = counted_gardens & profile.gardens.all()

    return render_to_response('cropcount/gardens/index.html', {
        'counted_gardens': counted_gardens.order_by('name'),
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
def add_garden(request):
    """Add a garden--either a new one, or one we've uploaded"""

    if request.method == 'POST':
        form = GardenForm(request.POST, user=request.user)
        if form.is_valid():
            garden = form.save()
            return redirect(garden_details, garden.id)

        uncounted_garden_form = UncountedGardenForm(request.POST)
        if uncounted_garden_form.is_valid():
            garden = uncounted_garden_form.cleaned_data['garden']
            return redirect(garden_details, garden.id)
    else:
        form = GardenForm(user=request.user)
        uncounted_garden_form = UncountedGardenForm(user=request.user)

    return render_to_response('cropcount/gardens/add.html', {
        'form': form,
        'uncounted_garden_form': uncounted_garden_form,
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
def garden_details(request, id):
    """Show details for a garden, let user add boxes"""

    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    beds = Box.objects.filter(garden=garden)
    patches = Patch.objects.filter(box__in=beds)

    if request.method == 'POST':
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save()
            return redirect(bed_details, box.id)
    else:
        form = BoxForm(initial={ 'garden': garden, 'name': _get_next_box_name(garden) })

    return render_to_response('cropcount/gardens/detail.html', {
        'garden': garden,
        'form': form,
        'area': beds.extra(select = {'total': 'sum(length * width)'})[0].total,
        'beds': beds.count(),
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
def bed_details(request, id):
    """Show bed details, let users add patches of plants to the current one"""

    bed = get_object_or_404(Box, pk=id)

    if request.method == 'POST':
        form = PatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(bed_details, id)
    else:
        #form = make_ajax_form(PatchForm(initial={ 'box': bed }), dict(variety='variety'))
        form = PatchForm(initial={ 'box': bed })

    return render_to_response('cropcount/beds/detail.html', {
        'bed': bed,
        'form': form
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
def delete_patch(request, id):
    patch = get_object_or_404(Patch, pk=id)
    bed_id = patch.box.id
    patch.delete()
    return redirect(bed_details, bed_id) 

@login_required
@in_section('cropcount')
def delete_bed(request, id):
    bed = get_object_or_404(Box, pk=id)
    garden_id = bed.garden.id
    bed.delete()
    return redirect(garden_details, garden_id) 

#
# Views that do not output HTML
#

@login_required
@garden_type_aware
@in_section('cropcount')
def complete_geojson(request):
    """Get GeoJSON for all gardens counted so far"""

    gardens = Garden.counted()

    type = request.session['garden_type']
    if type != 'all':
        gardens = gardens.filter(type=type)

    return HttpResponse(geojson.dumps(garden_collection(gardens)), mimetype='application/json')

#
# Utility functions
#
def _get_next_box_name(garden):
    """If each box name for this garden so far has been an integer, guess it's the next integer"""

    next_box_name = '1'
    box_names = Box.objects.filter(garden=garden).values_list('name', flat=True)
    if box_names:
        try:
            next_box_name = max([int(name) for name in box_names]) + 1
        except ValueError:
            next_box_name = ''

    return next_box_name

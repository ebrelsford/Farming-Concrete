import geojson

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Sum

from farmingconcrete.models import Garden
from cropcount.models import Box, Patch, GardenForm, BoxForm, PatchForm

@login_required
def index(request):
    """Home page for Crop Count. Show current stats, give access to next actions."""

    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM farmingconcrete_garden WHERE id IN (SELECT garden_id FROM cropcount_box)')
    counted_gardens = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(length * width) FROM cropcount_box')
    total_area = cursor.fetchone()[0]

    return render_to_response('cropcount/index.html', {
        'gardens': counted_gardens,
        'area': total_area,
        'plants': Patch.objects.all().aggregate(Sum('plants'))['plants__sum'],
        'recent_types': Patch.objects.all().order_by('-added')[:3],
    }, context_instance=RequestContext(request))

@login_required
def gardens(request):
    """Show counted gardens, let user add more"""

    return render_to_response('cropcount/gardens/index.html', {
        'counted_gardens': Garden.counted().order_by('name'),
    }, context_instance=RequestContext(request))

@login_required
def add_garden(request):
    """Add a garden--either a new one, or one we've uploaded"""

    if request.method == 'POST':
        form = GardenForm(request.POST)
        if form.is_valid():
            garden = form.save()
            return redirect(garden_details, garden.id)
    else:
        form = GardenForm()

    return render_to_response('cropcount/gardens/add.html', {
        'form': form,
        'uncounted': Garden.uncounted().order_by('name'),
    }, context_instance=RequestContext(request))

@login_required
def garden_details(request, id):
    """Show details for a garden, let user add boxes"""

    garden = get_object_or_404(Garden, pk=id)

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
    }, context_instance=RequestContext(request))

@login_required
def bed_details(request, id):
    """Show bed details, let users add patches of plants to the current one"""

    bed = get_object_or_404(Box, pk=id)

    if request.method == 'POST':
        form = PatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(bed_details, id)
    else:
        form = PatchForm(initial={ 'box': bed })

    return render_to_response('cropcount/beds/detail.html', {
        'bed': bed,
        'form': form
    }, context_instance=RequestContext(request))

@login_required
def delete_patch(request, id):
    patch = get_object_or_404(Patch, pk=id)
    bed_id = patch.box.id
    patch.delete()
    return redirect(bed_details, bed_id) 

@login_required
def delete_bed(request, id):
    bed = get_object_or_404(Box, pk=id)
    garden_id = bed.garden.id
    bed.delete()
    return redirect(garden_details, garden_id) 

#
# Views that do not output HTML
#

@login_required
def complete_geojson(request):
    """Get GeoJSON for all gardens counted so far"""

    return HttpResponse(
        geojson.dumps(geojson.FeatureCollection(features=[_get_feature(g) for g in Garden.counted()])),
        mimetype='application/json'
    )

#
# Utility functions
#

def _get_feature(garden):
    """Get a GeoJSON Feature for a garden"""

    return geojson.Feature(
        garden.id,
        geometry=geojson.Point(coordinates=(float(garden.longitude), float(garden.latitude)))
    )

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

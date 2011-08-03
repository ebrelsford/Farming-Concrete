import geojson
from datetime import date

import unicodecsv

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
from models import Box, Patch
from forms import UncountedGardenForm, BoxForm, PatchForm

from middleware.http import Http403

@login_required
@garden_type_aware
@in_section('cropcount')
def index(request):
    """Home page for Crop Count. Show current stats, give access to next actions."""
    garden_type = request.session['garden_type']

    counted_gardens = Garden.objects.exclude(box=None)
    beds = Box.objects.all()
    patches = Patch.objects.all()

    # filter more if we need to
    if garden_type != 'all':
        counted_gardens = counted_gardens.filter(type=garden_type)
        beds = beds.filter(garden__type=garden_type)
        patches = patches.filter(box__garden__type=garden_type)
    
    return render_to_response('cropcount/index.html', {
        'gardens': counted_gardens.count(),
        'area': beds.extra(select = {'total': 'sum(length * width)'})[0].total,
        'beds': beds.count(),
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'recent_types': patches.order_by('-added').values_list('variety__name', flat=True)[:3],
        'garden_type': garden_type,
    }, context_instance=RequestContext(request))

@login_required
@garden_type_aware
@in_section('cropcount')
def user_gardens(request):
    """Show the user's gardens"""
    type = request.session['garden_type']

    profile = request.user.get_profile()
    user_gardens = profile.gardens.all()
    if type != 'all':
        user_gardens = user_gardens.filter(type=type)

    return render_to_response('cropcount/gardens/user_gardens.html', {
        'user_gardens': user_gardens.order_by('name'),
        'user_garden_ids': user_gardens.values_list('id', flat=True),
    }, context_instance=RequestContext(request))

@login_required
@garden_type_aware
@in_section('cropcount')
def all_gardens(request):
    """Show all counted gardens"""
    type = request.session['garden_type']

    counted_gardens = Garden.counted()
    profile = request.user.get_profile()
    user_gardens = profile.gardens.all()
    if type != 'all':
        counted_gardens = counted_gardens.filter(type=type)
        user_gardens = user_gardens.filter(type=type)

    return render_to_response('cropcount/gardens/all_gardens.html', {
        'counted_gardens': counted_gardens.order_by('name'),
        'user_gardens': user_gardens,
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

    #if not request.user.has_perm('can_edit_any_garden'):
    profile = request.user.get_profile()
    user_gardens = profile.gardens.all()
    #counted_gardens = counted_gardens & profile.gardens.all()

    return render_to_response('cropcount/gardens/index.html', {
        'user_gardens': user_gardens.order_by('name'),
        'counted_gardens': counted_gardens.all().order_by('name'),
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
        try:
            most_recent_box = Box.objects.filter(garden=garden).order_by('-added')[0]
            length = "%d" % most_recent_box.length
            width = "%d" % most_recent_box.width
        except IndexError:
            length = ""
            width = ""

        form = BoxForm(initial={
            'garden': garden, 
            'added_by': request.user,
            'name': _get_next_box_name(garden),
            'length': length,
            'width': width,
        })

    return render_to_response('cropcount/gardens/detail.html', {
        'garden': garden,
        'bed_list': sorted(garden.box_set.all()),
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
        form = PatchForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(bed_details, id)
    else:
        form = PatchForm(initial={ 'box': bed, 'added_by': request.user }, user=request.user)

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

@login_required
def download_garden_cropcount_as_csv(request, id):
    garden = get_object_or_404(Garden, pk=id)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s Crop Count (%s).csv"' % (garden.name, date.today().strftime('%m-%d-%Y'))

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['bed', 'crop', 'plants', 'area (square feet)'])

    for bed in sorted(garden.box_set.all()):
        for patch in bed.patch_set.all():
            writer.writerow([
                bed.name,
                patch.variety.name,
                patch.plants or '',
                patch.area or '',
            ])

    return response

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

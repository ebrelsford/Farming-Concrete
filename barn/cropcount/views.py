from datetime import date

import unicodecsv

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic.base import TemplateView

from farmingconcrete.models import Garden, Variety
from farmingconcrete.forms import GardenForm
from farmingconcrete.decorators import garden_type_aware, in_section, year_in_session
from models import Box, Patch
from forms import UncountedGardenForm, BoxForm, PatchForm

from middleware.http import Http403
from settings import FARMINGCONCRETE_YEAR

def _patches(year=FARMINGCONCRETE_YEAR):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)

@login_required
@garden_type_aware
@in_section('cropcount')
@year_in_session
def index(request, year=None):
    """Home page for Crop Count. Show current stats, give access to next actions."""
    garden_type = request.session['garden_type']

    patches = _patches(year=year)
    if garden_type != 'all':
        patches = patches.filter(box__garden__type=garden_type)

    beds = Box.objects.filter(patch__in=patches).distinct()
    gardens = Garden.objects.filter(box__in=beds).distinct()
    
    return render_to_response('cropcount/index.html', {
        'gardens': gardens.count(),
        'area': sum([b.length * b.width for b in beds]),
        'beds': beds.count(),
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
        'recent_types': patches.order_by('-added').values_list('variety__name', flat=True)[:3],
        'garden_type': garden_type,
    }, context_instance=RequestContext(request))

@login_required
@garden_type_aware
@in_section('cropcount')
@year_in_session
def user_gardens(request, year=None):
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
@year_in_session
def all_gardens(request, year=None):
    """Show all counted gardens"""
    type = request.session['garden_type']

    counted_gardens = Garden.counted().filter(box__patch__added__year=year).distinct()
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
@year_in_session
def gardens(request, year=None):
    """Show counted gardens, let user add more"""

    type = request.session['garden_type']

    counted_gardens = Garden.counted().filter(box__patch__added__year=year).distinct()
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
@year_in_session
def add_garden(request, year=None):
    """Add a garden--either a new one, or one we've uploaded"""

    if request.method == 'POST':
        form = GardenForm(request.POST, user=request.user)
        if form.is_valid():
            garden = form.save()
            return redirect(garden_details, id=garden.id, year=year)

        uncounted_garden_form = UncountedGardenForm(request.POST)
        if uncounted_garden_form.is_valid():
            garden = uncounted_garden_form.cleaned_data['garden']
            return redirect(garden_details, id=garden.id, year=year)
    else:
        form = GardenForm(user=request.user)
        uncounted_garden_form = UncountedGardenForm(user=request.user)

    return render_to_response('cropcount/gardens/add.html', {
        'form': form,
        'uncounted_garden_form': uncounted_garden_form,
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
@year_in_session
def garden_details(request, id, year=None):
    """Show details for a garden, let user add boxes"""

    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    patches = _patches(year=year).filter(box__garden=garden)
    beds = Box.objects.filter(patch__in=patches).distinct()

    if request.method == 'POST':
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save()
            return redirect(bed_details, id=box.id, year=year)
    else:
        try:
            most_recent_box = Box.objects.filter(
                garden=garden,
                added__year=year,
            ).order_by('-added')[0]
            length = "%d" % most_recent_box.length
            width = "%d" % most_recent_box.width
        except IndexError:
            length = ""
            width = ""

        form = BoxForm(initial={
            'garden': garden, 
            'added_by': request.user,
            'name': _get_next_box_name(garden, year=year),
            'length': length,
            'width': width,
        })

    bed_added = beds.values_list('added', flat=True).order_by('added')
    bed_months = []
    for added in bed_added:
        month_name = added.strftime('%B')
        if month_name not in bed_months:
            bed_months.append(month_name)

    return render_to_response('cropcount/gardens/detail.html', {
        'garden': garden,
        'bed_list': sorted(beds),
        'form': form,
        'area': sum([b.length * b.width for b in beds]),
        'bed_months': bed_months,
        'beds': beds.count(),
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
@year_in_session
def summary(request, id=None, year=None):
    """Show cropcount for a garden, don't let user add boxes"""

    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    patches = _patches(year=year).filter(box__garden=garden)
    beds = Box.objects.filter(patch__in=patches).distinct()

    bed_added = beds.values_list('added', flat=True).order_by('added')
    bed_months = []
    for added in bed_added:
        month_name = added.strftime('%B')
        if month_name not in bed_months:
            bed_months.append(month_name)

    return render_to_response('cropcount/gardens/summary.html', {
        'garden': garden,
        'bed_list': sorted(beds),
        'area': sum([b.length * b.width for b in beds]),
        'bed_months': bed_months,
        'beds': beds.count(),
        'plants': patches.aggregate(Sum('plants'))['plants__sum'],
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
@year_in_session
def add_bed(request, id=None, year=None):
    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = request.user.get_profile()
        if garden not in profile.gardens.all():
            raise Http403

    if request.method == 'POST':
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save()
            return redirect(bed_details, id=box.id, year=year)
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
            'name': _get_next_box_name(garden, year=year),
            'length': length,
            'width': width,
        })

    patches = _patches(year=year).filter(box__garden=garden)
    beds = Box.objects.filter(patch__in=patches).distinct()

    bed_added = beds.values_list('added', flat=True).order_by('added')
    bed_months = []
    for added in bed_added:
        month_name = added.strftime('%B')
        if month_name not in bed_months:
            bed_months.append(month_name)

    return render_to_response('cropcount/beds/add.html', {
        'garden': garden,
        'bed_list': sorted(beds),
        'form': form,
        'area': sum([b.length * b.width for b in beds]),
        'bed_months': bed_months,
        'beds': beds.count(),
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
@year_in_session
def add_patch(request, bed_id=None, year=None):
    bed = get_object_or_404(Box, pk=bed_id)

    try:
        variety_id = request.GET['variety']
        variety = Variety.objects.get(id=variety_id)
    except Exception:
        variety = None

    if request.method == 'POST':
        form = PatchForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(bed_details, id=bed_id, year=year)
        else:
            try:
                variety = Variety.objects.get(id=form.data['variety'])
            except Exception:
                pass
    else:
        form = PatchForm(
            initial={ 
                'added_by': request.user,
                'box': bed,
                'variety': variety,
            }, 
            user=request.user
        )

    return render_to_response('cropcount/patches/add.html', {
        'bed': bed,
        'form': form,
        'variety': variety,
    }, context_instance=RequestContext(request))


@login_required
@in_section('cropcount')
@year_in_session
def bed_details(request, id, year=None):
    """Show bed details, let users add patches of plants to the current one"""

    bed = get_object_or_404(Box, pk=id)

    if request.method == 'POST':
        form = PatchForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(bed_details, id=id, year=year)
    else:
        form = PatchForm(initial={ 'box': bed, 'added_by': request.user }, user=request.user)

    return render_to_response('cropcount/beds/detail.html', {
        'bed': bed,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
@in_section('cropcount')
@year_in_session
def delete_patch(request, id, year=None):
    patch = get_object_or_404(Patch, pk=id)
    bed_id = patch.box.id
    patch.delete()
    return redirect(bed_details, id=bed_id, year=year) 

class ConfirmDeletePatchView(TemplateView):
    template_name = 'cropcount/patches/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmDeletePatchView, self).get_context_data(**kwargs)
        print kwargs
        context['patch_id'] = kwargs['id']
        return context

@login_required
@in_section('cropcount')
@year_in_session
def delete_bed(request, id, year=None):
    bed = get_object_or_404(Box, pk=id)
    garden_id = bed.garden.id
    bed.delete()
    return redirect(garden_details, id=garden_id, year=year) 

@login_required
@year_in_session
def download_garden_cropcount_as_csv(request, id, year=None):
    garden = get_object_or_404(Garden, pk=id)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s Crop Count (%s).csv"' % (garden.name, date.today().strftime('%m-%d-%Y'))

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['bed', 'crop', 'plants', 'area (square feet)'])

    patches = _patches(year=year).filter(box__garden=garden).distinct()
    beds = Box.objects.filter(patch__in=patches).distinct()

    for bed in sorted(beds):
        for patch in patches:
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
def _get_next_box_name(garden, year=FARMINGCONCRETE_YEAR):
    """
    If each box name for this garden so far has been an integer, guess we want
    the next integer.
    """
    next_box_name = '1'
    box_names = Box.objects.filter(
        garden=garden,
        added__year=year,
    ).values_list('name', flat=True)
    if box_names:
        try:
            next_box_name = max([int(name) for name in box_names]) + 1
        except ValueError:
            next_box_name = ''

    return next_box_name

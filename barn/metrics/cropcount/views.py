from datetime import date

import unicodecsv

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic.base import TemplateView

from farmingconcrete.models import Garden, Variety
from farmingconcrete.decorators import garden_type_aware, in_section, year_in_session
from ..views import IndexView
from .forms import BoxForm, PatchForm
from .models import Box, Patch

from middleware.http import Http403


def _patches(year=settings.FARMINGCONCRETE_YEAR):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)


class CropcountIndex(IndexView):
    model = Patch

    def get_default_year(self):
        return settings.FARMINGCONCRETE_YEAR

    def get_context_data(self, **kwargs):
        context = super(CropcountIndex, self).get_context_data(**kwargs)
        patches = self.get_records()

        # TODO Add garden_type back?

        beds = Box.objects.filter(patch__in=patches)
        gardens = Garden.objects.filter(box__in=beds)
        recent_types = patches.order_by('-added').values_list('variety__name',
                                                              flat=True)[:3],
        context.update({
            'area': sum([b.length * b.width for b in beds]),
            'beds': beds.count(),
            'gardens': gardens.count(),
            'plants': patches.aggregate(Sum('plants'))['plants__sum'],
            'recent_types': recent_types[0],
        })
        return context


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

    counted_gardens = Garden.counted().filter(
        box__patch__added__year=year
    ).distinct()
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

    counted_gardens = Garden.counted().filter(
        box__patch__added__year=year
    ).distinct()
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
            return redirect(bed_details, id=box.id)
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
            return redirect(bed_details, id=box.id)
    else:
        try:
            most_recent_box = Box.objects.filter(
                garden=garden
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
def add_patch(request, bed_id=None):
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
            return redirect(bed_details, id=bed_id)
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
            return redirect(bed_details, id=id)
    else:
        initial = {
            'added_by': request.user,
            'box': bed,
        }
        form = PatchForm(initial=initial, user=request.user)

    return render_to_response('cropcount/beds/detail.html', {
        'bed': bed,
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
@in_section('cropcount')
def delete_patch(request, id):
    patch = get_object_or_404(Patch, pk=id)
    bed_id = patch.box.id
    patch.delete()
    return redirect(bed_details, id=bed_id)


class ConfirmDeletePatchView(TemplateView):
    template_name = 'cropcount/patches/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmDeletePatchView, self).get_context_data(**kwargs)
        context['patch_id'] = kwargs['id']
        return context


@login_required
@in_section('cropcount')
@year_in_session
def delete_bed(request, id, year=None):
    bed = get_object_or_404(Box, pk=id)
    garden_id = bed.garden.id
    try:
        bed_year = bed.patch_set.all().order_by('added')[0].added.year
    except Exception:
        bed_year = year
    bed.delete()
    return redirect(garden_details, id=garden_id, year=bed_year)


@login_required
@year_in_session
def download_garden_cropcount_as_csv(request, id, year=None):
    garden = get_object_or_404(Garden, pk=id)
    filename = '%s Crop Count (%s).csv' % (
        garden.name,
        date.today().strftime('%m-%d-%Y'),
    )

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

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
def _get_next_box_name(garden, year=settings.FARMINGCONCRETE_YEAR):
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

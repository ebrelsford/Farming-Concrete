from datetime import date

import unicodecsv

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from accounts.utils import get_profile
from farmingconcrete.models import Garden
from farmingconcrete.decorators import garden_type_aware, in_section, year_in_session
from farmingconcrete.utils import garden_type_label
from farmingconcrete.views import FarmingConcreteYearMixin
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin, UserGardenView)
from .forms import BoxForm, PatchFormSet
from .models import Box, Patch

from middleware.http import Http403


def _patches(year=settings.FARMINGCONCRETE_YEAR):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)


class CropcountMixin(MetricMixin):
    def get_metric_name(self):
        return 'Crop Count'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class CropcountIndex(CropcountMixin, IndexView):
    metric_model = Patch

    def get_context_data(self, **kwargs):
        context = super(CropcountIndex, self).get_context_data(**kwargs)
        patches = self.get_records()

        # TODO Add garden_type back?

        beds = Box.objects.filter(patch__in=patches)
        gardens = Garden.objects.filter(box__in=beds)
        recent_types = patches.order_by('-added').values_list('crop__name',
                                                              flat=True)[:3],
        context.update({
            'area': sum([b.length * b.width for b in beds]),
            'beds': beds.count(),
            'gardens': gardens.count(),
            'plants': patches.filter(units='plants').aggregate(Sum('quantity'))['quantity__sum'],
            'recent_types': recent_types[0],
        })
        return context


class GardenDetails(CropcountMixin, GardenDetailAddRecordView):
    form_class = BoxForm
    metric_model = Patch
    success_message = 'Successfully added bed'
    template_name = 'metrics/cropcount/gardens/detail.html'

    def get_initial_box_dimensions(self, garden):
        try:
            most_recent_box = Box.objects.filter(
                garden=garden,
                added__year=self.get_year(),
            ).order_by('-added')[0]
            return "%d" % most_recent_box.length, "%d" % most_recent_box.width
        except IndexError:
            return '', ''

    def get_initial(self):
        garden = self.get_object()
        length, width = self.get_initial_box_dimensions(garden)

        initial = super(GardenDetails, self).get_initial()
        initial.update({
            'garden': garden,
            'added_by': self.request.user,
            'name': _get_next_box_name(garden, year=self.get_year()),
            'length': length,
            'width': width,
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(GardenDetails, self).get_context_data(**kwargs)

        garden = self.get_object()
        patches = self.get_records()
        beds = Box.objects.filter(patch__in=patches).distinct()

        if self.request.POST:
            context['patch_formset'] = PatchFormSet(self.request.POST,
                                                    self.request.FILES)
        else:
            context['patch_formset'] = PatchFormSet()

        context.update({
            'area': sum([b.length * b.width for b in beds]),
            'bed_list': sorted(beds),
            'beds': beds.count(),
            'form': self.get_form(self.form_class),
            'garden': garden,
            'plants': patches.filter(units='plants').aggregate(Sum('quantity'))['quantity__sum'],
            'records': sorted(beds),
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        patch_formset = context['patch_formset']
        if patch_formset.is_valid():
            patch_formset.instance = form.save()
            patch_formset.save()
            return super(GardenDetails, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse(self.get_metric()['garden_detail_url_name'], kwargs={
            'pk': self.object.pk,
        })


class CropcountUserGardenView(TitledPageMixin, CropcountMixin, UserGardenView):
    metric_model = Patch

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class CropcountAllGardensView(RecordsMixin, TitledPageMixin,
                              FarmingConcreteYearMixin, CropcountMixin,
                              AllGardensView):
    metric_model = Patch

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'All counted %s gardens' % garden_type_label(garden_type)


@login_required
@garden_type_aware
@in_section('cropcount')
@year_in_session
def gardens(request, year=None):
    """Show counted gardens, let user add more"""

    type = request.session.get('garden_type', 'all')

    counted_gardens = Garden.counted().filter(
        box__patch__added__year=year
    ).distinct()
    if type != 'all':
        counted_gardens = counted_gardens.filter(type=type)

    #if not request.user.has_perm('can_edit_any_garden'):
    profile = get_profile(request.user)
    user_gardens = profile.gardens.all()
    #counted_gardens = counted_gardens & profile.gardens.all()

    return render_to_response('metrics/cropcount/gardens/index.html', {
        'user_gardens': user_gardens.order_by('name'),
        'counted_gardens': counted_gardens.all().order_by('name'),
    }, context_instance=RequestContext(request))


@login_required
@in_section('cropcount')
@year_in_session
def summary(request, id=None, year=None):
    """Show cropcount for a garden, don't let user add boxes"""

    garden = get_object_or_404(Garden, pk=id)

    if not request.user.has_perm('can_edit_any_garden'):
        profile = get_profile(request.user)
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

    return render_to_response('metrics/cropcount/gardens/summary.html', {
        'garden': garden,
        'bed_list': sorted(beds),
        'area': sum([b.length * b.width for b in beds]),
        'bed_months': bed_months,
        'beds': beds.count(),
        'plants': patches.filter(units='plants').aggregate(Sum('quantity'))['quantity__sum'],
    }, context_instance=RequestContext(request))


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
    return redirect('cropcount_garden_details', pk=garden_id, year=bed_year)


@login_required
@year_in_session
def download_garden_cropcount_as_csv(request, pk=None, year=None):
    garden = get_object_or_404(Garden, pk=pk)
    filename = '%s Crop Count (%s).csv' % (
        garden.name,
        date.today().strftime('%m-%d-%Y'),
    )

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow(['bed', 'crop', 'crop variety', 'quantity', 'units'])

    patches = _patches(year=year).filter(box__garden=garden).distinct()
    beds = Box.objects.filter(patch__in=patches).distinct()

    for bed in sorted(beds):
        for patch in patches:
            try:
                crop_variety = patch.crop_variety.name
            except Exception:
                crop_variety = ''
            writer.writerow([
                bed.name,
                patch.crop.name,
                crop_variety,
                patch.quantity,
                patch.units,
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

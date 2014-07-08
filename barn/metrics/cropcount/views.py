from datetime import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from accounts.utils import get_profile
from farmingconcrete.models import Garden
from farmingconcrete.views import FarmingConcreteYearMixin
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin)
from .forms import BoxForm, PatchFormSet
from .models import Box, Patch

from middleware.http import Http403


def _patches(year=datetime.now().year):
    """Get current patches"""
    return Patch.objects.filter(added__year=year)


class CropcountMixin(MetricMixin):
    metric_model = Patch

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


class CropcountAllGardensView(RecordsMixin, TitledPageMixin,
                              FarmingConcreteYearMixin, CropcountMixin,
                              AllGardensView):
    metric_model = Patch

    def get_title(self):
        return 'All counted gardens'


@login_required
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
def delete_bed(request, id, year=None):
    bed = get_object_or_404(Box, pk=id)
    garden_id = bed.garden.id
    try:
        bed_year = bed.patch_set.all().order_by('added')[0].added.year
    except Exception:
        bed_year = year
    bed.delete()
    return redirect('cropcount_garden_details', pk=garden_id, year=bed_year)


class CropcountCSV(CropcountMixin, MetricGardenCSVView):

    def get_fields(self):
        return super(CropcountCSV, self).get_fields() + (
            'bed',
            'crop',
            'crop_variety',
            'quantity',
            'units',
        )

    def get_rows(self):
        for record in self.get_records():
            def get_cell(field):
                if field == 'bed' and record.box:
                    return record.box.name
                if field == 'crop_variety':
                    if record.crop_variety:
                        return record.crop_variety.name
                    else:
                        return ''
                try:
                    return getattr(record, field)
                except Exception:
                    return ''
            yield dict(map(lambda f: (f, get_cell(f)), self.get_fields()))


#
# Utility functions
#
def _get_next_box_name(garden, year=datetime.now().year):
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

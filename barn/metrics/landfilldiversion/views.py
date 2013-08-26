from datetime import date

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import (CSVView, LoginRequiredMixin,
                           SuccessMessageFormMixin, TitledPageMixin)
from ..views import (AllGardensView, GardenMixin, IndexView, MetricMixin,
                     RecordsMixin, UserGardenView)
from .forms import LandfillDiversionVolumeForm, LandfillDiversionWeightForm
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class WeightMixin(MetricMixin):
    metric_model = LandfillDiversionWeight

    def get_metric_name(self):
        return 'Landfill Diversion by Weight'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class WeightIndex(WeightMixin, IndexView):
    metric_model = LandfillDiversionWeight


class WeightAllGardensView(RecordsMixin, TitledPageMixin, WeightMixin,
                           AllGardensView):
    metric_model = LandfillDiversionWeight

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens weighing landfill diversion' %
                garden_type_label(garden_type))


class WeightUserGardensView(TitledPageMixin, WeightMixin, UserGardenView):
    metric_model = LandfillDiversionWeight

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class WeightGardenDetails(SuccessMessageFormMixin, WeightMixin, GardenMixin,
                          FormView):
    form_class = LandfillDiversionWeightForm
    metric_model = LandfillDiversionWeight
    template_name = 'metrics/landfilldiversion/gardens/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(WeightGardenDetails, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(WeightGardenDetails, self).post(request, *args, **kwargs)

    def get_success_message(self):
        return 'Successfully added %.1f pounds to %s' % (self.record.weight,
                                                         self.object)

    def get_success_url(self):
        return reverse('landfilldiversion_weight_garden_details', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        self.record = form.save()
        return super(WeightGardenDetails, self).form_valid(form)

    def get_initial(self):
        garden = self.object

        initial = super(WeightGardenDetails, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'garden': garden,
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(WeightGardenDetails, self).get_context_data(**kwargs)

        garden = self.object
        records = self.get_records()

        context.update({
            'form': self.get_form(self.form_class),
            'garden': garden,
            'records': records.order_by('recorded'),
            'summary': LandfillDiversionWeight.summarize(records),
        })
        return context


class WeightGardenCSV(WeightMixin, GardenMixin, LoginRequiredMixin, CSVView):

    def get(self, request, *args, **kwargs):
        self.object = self.garden = self.get_object()
        return super(WeightGardenCSV, self).get(request, *args, **kwargs)

    def get_fields(self):
        return ('weight', 'recorded',)

    def get_rows(self):
        for record in self.get_records():
            yield dict(map(lambda f: (f, getattr(record, f)), self.get_fields()))

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - landfill diversion by weight' % self.garden.name


class VolumeMixin(MetricMixin):
    metric_model = LandfillDiversionVolume

    def get_metric_name(self):
        return 'Landfill Diversion by Volume'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class VolumeIndex(VolumeMixin, IndexView):
    metric_model = LandfillDiversionVolume
    template_name = 'metrics/landfilldiversion/volume/index.html'


class VolumeGardenDetails(SuccessMessageFormMixin, VolumeMixin, GardenMixin,
                          FormView):
    form_class = LandfillDiversionVolumeForm
    metric_model = LandfillDiversionVolume
    template_name = 'metrics/landfilldiversion/volume/garden_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(VolumeGardenDetails, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(VolumeGardenDetails, self).post(request, *args, **kwargs)

    def get_success_message(self):
        return 'Successfully added %.1f gallons to %s' % (self.record.volume,
                                                          self.object)

    def get_success_url(self):
        return reverse('landfilldiversion_volume_garden_details', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        self.record = form.save()
        return super(VolumeGardenDetails, self).form_valid(form)

    def get_initial(self):
        garden = self.object

        initial = super(VolumeGardenDetails, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'garden': garden,
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(VolumeGardenDetails, self).get_context_data(**kwargs)

        garden = self.object
        records = self.get_records()

        context.update({
            'form': self.get_form(self.form_class),
            'garden': garden,
            'records': records.order_by('recorded'),
            'summary': LandfillDiversionVolume.summarize(records),
        })
        return context


class VolumeAllGardensView(RecordsMixin, TitledPageMixin, VolumeMixin,
                           AllGardensView):
    metric_model = LandfillDiversionVolume

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring landfill diversion by volume' %
                garden_type_label(garden_type))


class VolumeUserGardensView(TitledPageMixin, VolumeMixin, UserGardenView):
    metric_model = LandfillDiversionVolume

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class VolumeGardenCSV(VolumeMixin, GardenMixin, LoginRequiredMixin, CSVView):

    def get(self, request, *args, **kwargs):
        self.object = self.garden = self.get_object()
        return super(VolumeGardenCSV, self).get(request, *args, **kwargs)

    def get_fields(self):
        return ('volume', 'recorded',)

    def get_rows(self):
        for record in self.get_records():
            yield dict(map(lambda f: (f, getattr(record, f)), self.get_fields()))

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - landfill diversion by volume' % self.garden.name

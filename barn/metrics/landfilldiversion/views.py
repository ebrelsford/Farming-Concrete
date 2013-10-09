from datetime import date

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import (CSVView, LoginRequiredMixin,
                           SuccessMessageFormMixin, TitledPageMixin)
from ..views import (AllGardensView, GardenDetailAddRecordView, GardenMixin,
                     IndexView, MetricGardenCSVView, MetricMixin, RecordsMixin,
                     UserGardenView)
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
    template_name = 'metrics/landfilldiversion/weight/index.html'


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


class WeightGardenDetails(WeightMixin, GardenDetailAddRecordView):
    form_class = LandfillDiversionWeightForm
    template_name = 'metrics/landfilldiversion/weight/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f pounds to %s' % (self.record.weight,
                                                         self.object)

    def get_initial(self):
        initial = super(WeightGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class WeightGardenCSV(WeightMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('weight', 'recorded',)

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


class VolumeGardenDetails(VolumeMixin, GardenDetailAddRecordView):
    form_class = LandfillDiversionVolumeForm
    template_name = 'metrics/landfilldiversion/volume/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f gallons to %s' % (self.record.volume,
                                                          self.object)

    def get_initial(self):
        initial = super(VolumeGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


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


class VolumeGardenCSV(VolumeMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('volume', 'recorded',)

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - landfill diversion by volume' % self.garden.name

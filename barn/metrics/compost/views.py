from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricGardenCSVView, MetricMixin, RecordsMixin,
                     UserGardenView)
from .forms import CompostProductionVolumeForm, CompostProductionWeightForm
from .models import CompostProductionVolume, CompostProductionWeight


class WeightMixin(MetricMixin):
    metric_model = CompostProductionWeight

    def get_metric_name(self):
        return 'Compost Production by Weight'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class WeightIndex(WeightMixin, IndexView):
    metric_model = CompostProductionWeight
    template_name = 'metrics/compost/weight/index.html'


class WeightAllGardensView(RecordsMixin, TitledPageMixin, WeightMixin,
                           AllGardensView):
    metric_model = CompostProductionWeight

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens weighing compost production' %
                garden_type_label(garden_type))


class WeightUserGardensView(TitledPageMixin, WeightMixin, UserGardenView):
    metric_model = CompostProductionWeight

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class WeightGardenDetails(WeightMixin, GardenDetailAddRecordView):
    form_class = CompostProductionWeightForm
    template_name = 'metrics/compost/weight/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f pounds to %s' % (self.record.weight,
                                                         self.object)


class WeightGardenCSV(WeightMixin, MetricGardenCSVView):

    def get_fields(self):
        return super(WeightGardenCSV, self).get_fields() + ('weight',)


class VolumeMixin(MetricMixin):
    metric_model = CompostProductionVolume

    def get_metric_name(self):
        return 'Compost Production by Volume'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class VolumeIndex(VolumeMixin, IndexView):
    metric_model = CompostProductionVolume
    template_name = 'metrics/compost/volume/index.html'


class VolumeGardenDetails(VolumeMixin, GardenDetailAddRecordView):
    form_class = CompostProductionVolumeForm
    metric_model = CompostProductionVolume
    template_name = 'metrics/compost/volume/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f gallons to %s' % (self.record.volume,
                                                          self.object)


class VolumeAllGardensView(RecordsMixin, TitledPageMixin, VolumeMixin,
                           AllGardensView):
    metric_model = CompostProductionVolume

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring compost production by volume' %
                garden_type_label(garden_type))


class VolumeUserGardensView(TitledPageMixin, VolumeMixin, UserGardenView):
    metric_model = CompostProductionVolume

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class VolumeGardenCSV(VolumeMixin, MetricGardenCSVView):

    def get_fields(self):
        return super(VolumeGardenCSV, self).get_fields() + ('volume',)

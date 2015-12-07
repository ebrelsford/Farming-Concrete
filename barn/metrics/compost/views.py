from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin)
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
        return 'All gardens weighing compost production'


class WeightGardenDetails(WeightMixin, GardenDetailAddRecordView):
    form_class = CompostProductionWeightForm
    template_name = 'metrics/compost/weight/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f %s to %s' % (self.record.weight_new.value,
                                                     self.record.weight_new.unit,
                                                     self.object)


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
        return 'All gardens measuring compost production by volume'

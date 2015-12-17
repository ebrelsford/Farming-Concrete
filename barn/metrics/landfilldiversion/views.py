from django.views.generic import View

from braces.views import JSONResponseMixin

from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin)
from .forms import LandfillDiversionVolumeForm, LandfillDiversionWeightForm
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class WeightMixin(MetricMixin):
    metric_model = LandfillDiversionWeight

    def get_metric_name(self):
        return 'Landfill Waste Diversion by Weight'

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
        return 'All gardens weighing landfill diversion'


class WeightGardenDetails(WeightMixin, GardenDetailAddRecordView):
    form_class = LandfillDiversionWeightForm
    template_name = 'metrics/landfilldiversion/weight/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f %s to %s' % (self.record.weight.value,
                                                     self.record.weight.unit,
                                                     self.object)


class VolumeMixin(MetricMixin):
    metric_model = LandfillDiversionVolume

    def get_metric_name(self):
        return 'Landfill Waste Diversion by Volume'

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
        return 'Successfully added %.1f %s to %s' % (self.record.volume_new.value,
                                                     self.record.volume_new.unit,
                                                     self.object)


class VolumeAllGardensView(RecordsMixin, TitledPageMixin, VolumeMixin,
                           AllGardensView):
    metric_model = LandfillDiversionVolume

    def get_title(self):
        return 'All gardens measuring landfill diversion by volume'


class VolumeSummaryJSON(VolumeMixin, JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        records = self.metric_model.objects.all().order_by('recorded')
        def make_row(record):
            return {
                'date': record.recorded,
                'volume': float(record.volume),
            }
        data = [make_row(r) for r in records]
        return self.render_json_response(data)

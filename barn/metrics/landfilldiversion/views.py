from django.views.generic import View

from braces.views import JSONResponseMixin

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricGardenCSVView, MetricMixin, RecordsMixin,
                     UserGardenView)
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


class WeightGardenCSV(WeightMixin, MetricGardenCSVView):

    def get_fields(self):
        return super(WeightGardenCSV, self).get_fields() + ('weight',)


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
        return 'Successfully added %.1f gallons to %s' % (self.record.volume,
                                                          self.object)


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
        return super(VolumeGardenCSV, self).get_fields() + ('volume',)


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

from farmingconcrete.models import Garden

from ..views import (GardenDetailAddRecordView, IndexView, MetricGardenCSVView,
                     MetricMixin)

from .forms import RainwaterHarvestForm
from .models import RainwaterHarvest
from .utils import calculate_rainwater_gallons


class RainwaterHarvestMixin(MetricMixin):
    metric_model = RainwaterHarvest

    def get_metric_name(self):
        return 'Rainwater Harvesting'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class RainwaterHarvestIndex(RainwaterHarvestMixin, IndexView):
    template_name = 'metrics/rainwater/harvest/index.html'


class RainwaterHarvestGardenDetails(RainwaterHarvestMixin,
                                    GardenDetailAddRecordView):
    form_class = RainwaterHarvestForm
    template_name = 'metrics/rainwater/harvest/garden_detail.html'

    def calculate_volume(self, garden, record):
        return calculate_rainwater_gallons(
            [garden.latitude, garden.longitude],
            float(record.roof_length),
            float(record.roof_width),
            record.recorded_start,
            record.recorded
        )

    def form_valid(self, form):
        self.record = form.save()
        self.record.volume = self.calculate_volume(self.object, self.record)
        self.record.save()
        return super(RainwaterHarvestGardenDetails, self).form_valid(form)

    def get_success_message(self):
        return 'Successfully added %.1f gallons to %s' % (
            self.record.volume or 0,
            self.object,
        )


class RainwaterHarvestGardenCSV(RainwaterHarvestMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('roof_length', 'roof_width', 'volume', 'recorded_start',
                'recorded',)

from farmingconcrete.models import Garden

from ..views import GardenDetailAddRecordView, IndexView, MetricMixin

from .forms import RainwaterHarvestForm
from .models import RainwaterHarvest


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

    def get_success_message(self):
        return 'Successfully added %.1f gallons to %s' % (
            self.record.volume or 0,
            self.object,
        )

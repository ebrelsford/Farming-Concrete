from farmingconcrete.models import Garden

from ..views import GardenDetailAddRecordView, MetricMixin

from .forms import DonationForm
from .models import Donation


class DonationMixin(MetricMixin):
    metric_model = Donation

    def get_metric_name(self):
        return 'Donations of Food'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class DonationGardenDetails(DonationMixin, GardenDetailAddRecordView):
    form_class = DonationForm
    template_name = 'metrics/donations/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f pounds to %s' % (
            self.record.pounds or 0,
            self.object,
        )

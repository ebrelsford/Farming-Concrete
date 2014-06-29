from farmingconcrete.models import Garden

from ..views import GardenDetailAddRecordView, MetricGardenCSVView, MetricMixin

from .forms import SaleForm
from .models import Sale


class SaleMixin(MetricMixin):
    metric_model = Sale

    def get_metric_name(self):
        return 'Market Sales'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class SaleGardenDetails(SaleMixin, GardenDetailAddRecordView):
    form_class = SaleForm
    template_name = 'metrics/sales/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added sale to %s' % (self.object,)


class SaleGardenCSV(SaleMixin, MetricGardenCSVView):

    def get_fields(self):
        return super(SaleGardenCSV, self).get_fields() + (
            'product',
            'unit',
            'unit_price',
            'units_sold',
            'total_price',
        )

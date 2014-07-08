from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin)
from .forms import YumYuckForm
from .models import YumYuck


class YumYuckMixin(MetricMixin):
    metric_model = YumYuck

    def get_metric_name(self):
        return 'Changes in Attitude: Yum & Yuck'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class YumYuckIndex(YumYuckMixin, IndexView):
    template_name = 'metrics/yumyuck/change/index.html'


class YumYuckAllGardensView(RecordsMixin, TitledPageMixin, YumYuckMixin,
                            AllGardensView):

    def get_title(self):
        return 'All gardens measuring yum and yuck'


class YumYuckGardenDetails(YumYuckMixin, GardenDetailAddRecordView):
    form_class = YumYuckForm
    template_name = 'metrics/yumyuck/change/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added yum and yuck record to %s' % (
            self.object,
        )


class YumYuckGardenCSV(YumYuckMixin, MetricGardenCSVView):

    def get_fields(self):
        return super(YumYuckGardenCSV, self).get_fields() + (
            'crop',
            'yum_before',
            'yuck_before',
            'yum_after',
            'yuck_after',
        )

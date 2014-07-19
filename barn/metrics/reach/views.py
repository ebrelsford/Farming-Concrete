from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin)
from .forms import ProgramReachForm
from .models import ProgramReach


class ProgramReachMixin(MetricMixin):
    metric_model = ProgramReach

    def get_metric_name(self):
        return 'Reach of Programs'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class ProgramReachIndex(ProgramReachMixin, IndexView):
    template_name = 'metrics/reach/program/index.html'


class ProgramReachAllGardensView(RecordsMixin, TitledPageMixin,
                                 ProgramReachMixin, AllGardensView):

    def get_title(self):
        return 'All gardens measuring program reach'


class ProgramReachGardenDetails(ProgramReachMixin, GardenDetailAddRecordView):
    form_class = ProgramReachForm
    template_name = 'metrics/reach/program/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added program reach record to %s' % (
            self.object,
        )

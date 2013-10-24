from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import YumYuckForm
from .models import YumYuck


class YumYuckMixin(MetricMixin):
    metric_model = YumYuck

    def get_metric_name(self):
        return 'Yum and Yuck'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class YumYuckIndex(YumYuckMixin, IndexView):
    template_name = 'metrics/yumyuck/change/index.html'


class YumYuckAllGardensView(RecordsMixin, TitledPageMixin, YumYuckMixin,
                            AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring yum and yuck' %
                garden_type_label(garden_type))


class YumYuckUserGardensView(TitledPageMixin, YumYuckMixin, UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class YumYuckGardenDetails(YumYuckMixin, GardenDetailAddRecordView):
    form_class = YumYuckForm
    template_name = 'metrics/yumyuck/change/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added yum and yuck record to %s' % (
            self.object,
        )

    def get_initial(self):
        initial = super(YumYuckGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class YumYuckGardenCSV(YumYuckMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('recorded', 'vegetable', 'yum_before', 'yuck_before',
                'yum_after', 'yuck_after',)

from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import ProgramReachForm
from .models import ProgramReach


class ProgramReachMixin(MetricMixin):
    metric_model = ProgramReach

    def get_metric_name(self):
        return 'Program Reach'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class ProgramReachIndex(ProgramReachMixin, IndexView):
    template_name = 'metrics/reach/program/index.html'


class ProgramReachAllGardensView(RecordsMixin, TitledPageMixin,
                                 ProgramReachMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring program reach' %
                garden_type_label(garden_type))


class ProgramReachUserGardensView(TitledPageMixin, ProgramReachMixin,
                                  UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class ProgramReachGardenDetails(ProgramReachMixin, GardenDetailAddRecordView):
    form_class = ProgramReachForm
    template_name = 'metrics/reach/program/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added program reach record to %s' % (
            self.object,
        )

    def get_initial(self):
        initial = super(ProgramReachGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class ProgramReachGardenCSV(ProgramReachMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('recorded_start', 'recorded', 'name', 'hours_each_day',
                'collaborated_with_organization', 'collaboration_first',
                'age_10', 'age_10_14', 'age_15_19', 'age_20_24', 'age_25_34',
                'age_35_44', 'age_45_54', 'age_55_64', 'age_65', 'gender_male',
                'gender_female', 'gender_other', 'zipcode_inside',
                'zipcode_outside', 'features',)

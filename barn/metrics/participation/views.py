from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import HoursByGeographyForm#, HoursByTaskForm
from .models import HoursByGeography#, HoursByTask


class HoursByGeographyMixin(MetricMixin):
    metric_model = HoursByGeography

    def get_metric_name(self):
        return 'Participation Hours by Geography'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class HoursByGeographyIndex(HoursByGeographyMixin, IndexView):
    template_name = 'metrics/participation/geography/index.html'


class HoursByGeographyAllGardensView(RecordsMixin, TitledPageMixin,
                                     HoursByGeographyMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring participation by geography' %
                garden_type_label(garden_type))


class HoursByGeographyUserGardensView(TitledPageMixin, HoursByGeographyMixin,
                                      UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class HoursByGeographyGardenDetails(HoursByGeographyMixin,
                                    GardenDetailAddRecordView):
    form_class = HoursByGeographyForm
    template_name = 'metrics/participation/geography/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f hours to %s' % (self.record.hours,
                                                        self.object)

    def get_initial(self):
        initial = super(HoursByGeographyGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class HoursByGeographyGardenCSV(HoursByGeographyMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('hours', 'recorded_start', 'recorded',)

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - hours by geography' % self.garden.name

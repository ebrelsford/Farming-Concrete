from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import RecipeTallyForm
from .models import RecipeTally


class RecipeTallyMixin(MetricMixin):
    metric_model = RecipeTally

    def get_metric_name(self):
        return 'Recipe Tally'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class RecipeTallyIndex(RecipeTallyMixin, IndexView):
    template_name = 'metrics/recipes/tally/index.html'


class RecipeTallyAllGardensView(RecordsMixin, TitledPageMixin,
                                RecipeTallyMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens tallying recipes' %
                garden_type_label(garden_type))


class RecipeTallyUserGardensView(TitledPageMixin, RecipeTallyMixin,
                                 UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class RecipeTallyGardenDetails(RecipeTallyMixin, GardenDetailAddRecordView):
    form_class = RecipeTallyForm
    template_name = 'metrics/recipes/tally/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added recipe tally record to %s' % (
            self.object,
        )

    def get_initial(self):
        initial = super(RecipeTallyGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class RecipeTallyGardenCSV(RecipeTallyMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('recorded',)

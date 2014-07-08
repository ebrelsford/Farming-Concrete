from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin)
from .forms import RecipeTallyForm
from .models import RecipeTally


class RecipeTallyMixin(MetricMixin):
    metric_model = RecipeTally

    def get_metric_name(self):
        return 'Healthy Eating'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class RecipeTallyIndex(RecipeTallyMixin, IndexView):
    template_name = 'metrics/recipes/tally/index.html'


class RecipeTallyAllGardensView(RecordsMixin, TitledPageMixin,
                                RecipeTallyMixin, AllGardensView):

    def get_title(self):
        return 'All %s gardens tallying recipes'


class RecipeTallyGardenDetails(RecipeTallyMixin, GardenDetailAddRecordView):
    form_class = RecipeTallyForm
    template_name = 'metrics/recipes/tally/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added recipe tally record to %s' % (
            self.object,
        )


class RecipeTallyGardenCSV(RecipeTallyMixin, MetricGardenCSVView):

    def get_fields(self):
        parent_fields =  super(RecipeTallyGardenCSV, self).get_fields()
        return ('recorded_start',) + parent_fields + ('recipes_count',)

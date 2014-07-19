from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin)
from .forms import SmartsAndSkillsForm
from .models import SmartsAndSkills


class SmartsAndSkillsMixin(MetricMixin):
    metric_model = SmartsAndSkills

    def get_metric_name(self):
        return 'Skills & Knowledge in the Garden'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class SmartsAndSkillsIndex(SmartsAndSkillsMixin, IndexView):
    template_name = 'metrics/skills/smarts/index.html'


class SmartsAndSkillsAllGardensView(RecordsMixin, TitledPageMixin,
                                    SmartsAndSkillsMixin, AllGardensView):

    def get_title(self):
        return 'All gardens measuring smarts and skills'


class SmartsAndSkillsGardenDetails(SmartsAndSkillsMixin,
                                   GardenDetailAddRecordView):
    form_class = SmartsAndSkillsForm
    template_name = 'metrics/skills/smarts/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added smarts and skills record to %s' % (
            self.object,
        )

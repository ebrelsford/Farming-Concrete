from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import SmartsAndSkillsForm
from .models import SmartsAndSkills


class SmartsAndSkillsMixin(MetricMixin):
    metric_model = SmartsAndSkills

    def get_metric_name(self):
        return 'Smarts and Skills'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class SmartsAndSkillsIndex(SmartsAndSkillsMixin, IndexView):
    template_name = 'metrics/skills/smarts/index.html'


class SmartsAndSkillsAllGardensView(RecordsMixin, TitledPageMixin,
                                    SmartsAndSkillsMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring smarts and skills' %
                garden_type_label(garden_type))


class SmartsAndSkillsUserGardensView(TitledPageMixin, SmartsAndSkillsMixin,
                                     UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class SmartsAndSkillsGardenDetails(SmartsAndSkillsMixin,
                                   GardenDetailAddRecordView):
    form_class = SmartsAndSkillsForm
    template_name = 'metrics/skills/smarts/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added smarts and skills record to %s' % (
            self.object,
        )

    def get_initial(self):
        initial = super(SmartsAndSkillsGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class SmartsAndSkillsGardenCSV(SmartsAndSkillsMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('recorded', 'photo', 'participants', 'skills_shared',
                'concepts_shared', 'projects_proposed', 'ideas_to_learn',
                'intentions_to_collaborate',)

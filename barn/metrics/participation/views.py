from datetime import date
import json

from django.http import HttpResponse
from django.views.generic import CreateView

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import (LoginRequiredMixin, PermissionRequiredMixin,
                           TitledPageMixin)
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import (HoursByGeographyForm, HoursByProjectForm, HoursByTaskForm,
                    ProjectForm)
from .models import HoursByGeography, HoursByProject, HoursByTask, Project


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


class HoursByTaskMixin(MetricMixin):
    metric_model = HoursByTask

    def get_metric_name(self):
        return 'Participation Hours by Task'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class HoursByTaskIndex(HoursByTaskMixin, IndexView):
    template_name = 'metrics/participation/task/index.html'


class HoursByTaskAllGardensView(RecordsMixin, TitledPageMixin,
                                HoursByTaskMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring participation by task' %
                garden_type_label(garden_type))


class HoursByTaskUserGardensView(TitledPageMixin, HoursByTaskMixin,
                                 UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class HoursByTaskGardenDetails(HoursByTaskMixin, GardenDetailAddRecordView):
    form_class = HoursByTaskForm
    template_name = 'metrics/participation/task/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f hours to %s' % (self.record.hours,
                                                        self.object)

    def get_initial(self):
        initial = super(HoursByTaskGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class HoursByTaskGardenCSV(HoursByTaskMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('hours', 'task', 'recorded_start', 'recorded',)

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - hours by task' % self.garden.name


class HoursByProjectMixin(MetricMixin):
    metric_model = HoursByProject

    def get_metric_name(self):
        return 'Participation Hours by Project'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class HoursByProjectIndex(HoursByProjectMixin, IndexView):
    template_name = 'metrics/participation/project/index.html'


class HoursByProjectAllGardensView(RecordsMixin, TitledPageMixin,
                                   HoursByProjectMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring participation by project' %
                garden_type_label(garden_type))


class HoursByProjectUserGardensView(TitledPageMixin, HoursByProjectMixin,
                                    UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class HoursByProjectGardenDetails(HoursByProjectMixin,
                                  GardenDetailAddRecordView):
    form_class = HoursByProjectForm
    template_name = 'metrics/participation/project/garden_detail.html'

    def get_success_message(self):
        return 'Successfully added %.1f hours to %s' % (self.record.hours,
                                                        self.object)

    def get_initial(self):
        initial = super(HoursByProjectGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
            # TODO get last recorded project
        })
        return initial


class HoursByProjectGardenCSV(HoursByProjectMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('hours', 'project', 'recorded',)

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - hours by project' % self.garden.name


class CreateProjectView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    form_class = ProjectForm
    model = Project
    permission = 'participation.add_project'
    template_name = 'metrics/participation/project/project_form.html'

    def get_existing_project(self, garden, name):
        try:
            return Project.objects.get(garden=garden, name=name)
        except Exception:
            return None

    def form_valid(self, form):
        # Check for project with the given name, first
        project = self.get_existing_project(form.cleaned_data['garden'],
                                            form.cleaned_data['name'])
        if not project:
            project = self.object = form.save()
        return HttpResponse(json.dumps({
            'name': project.name,
            'pk': project.pk,
        }), content_type='application/json')

from datetime import date
import json

from django.forms.models import inlineformset_factory
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
                    ProjectForm, ProjectHoursForm, TaskHoursForm)
from .models import (HoursByGeography, HoursByProject, HoursByTask, Project,
                     ProjectHours, Task, TaskHours)


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
        return 'Successfully added hours by task to %s' % self.object

    def get_initial_task_hours(self):
        initial = []
        for task in Task.objects.all():
            initial.append({
                'task': task,
                'hours': 0,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super(HoursByTaskGardenDetails, self).get_context_data(**kwargs)

        TaskHoursFormSet = inlineformset_factory(HoursByTask, TaskHours,
            can_delete=False,
            extra=Task.objects.count(),
            form=TaskHoursForm,
        )
        if self.request.POST:
            context['taskhours_formset'] = TaskHoursFormSet(self.request.POST)
        else:
            context['taskhours_formset'] = TaskHoursFormSet(
                initial=self.get_initial_task_hours(),
            )
        context['tasks'] = Task.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        taskhours_formset = context['taskhours_formset']
        if taskhours_formset.is_valid():
            taskhours_formset.instance = form.save()
            taskhours_formset.save()
            return super(HoursByTaskGardenDetails, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        initial = super(HoursByTaskGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial


class HoursByTaskGardenCSV(HoursByTaskMixin, MetricGardenCSVView):

    def get_fields(self):
        tasks = [task.name for task in Task.objects.all()]
        return ['recorded_start', 'recorded',] + tasks

    def get_rows(self):
        for record in self.get_records():
            def get_cell(field):
                try:
                    return getattr(record, field)
                except Exception:
                    try:
                        # Maybe it's a task name
                        return record[field].hours
                    except Exception:
                        return 0
            yield dict(map(lambda f: (f, get_cell(f)), self.get_fields()))


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
        return 'Successfully added project hours to %s' % self.object

    def get_initial(self):
        initial = super(HoursByProjectGardenDetails, self).get_initial()
        initial.update({
            'recorded': date.today(), # TODO get last recorded date if there is one
            # TODO get last recorded project
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(HoursByProjectGardenDetails, self).get_context_data(**kwargs)

        ProjectHoursFormSet = inlineformset_factory(HoursByProject, ProjectHours,
            can_delete=False,
            extra=1,
            form=ProjectHoursForm,
        )
        if self.request.POST:
            context['projecthours_formset'] = ProjectHoursFormSet(self.request.POST,
                initial=[{
                    'garden': self.object,
                }]
            )
        else:
            context['projecthours_formset'] = ProjectHoursFormSet(
                initial=[{
                    'garden': self.object,
                }]
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        projecthours_formset = context['projecthours_formset']
        if projecthours_formset.is_valid():
            projecthours_formset.instance = form.save()
            projecthours_formset.save()
            return super(HoursByProjectGardenDetails, self).form_valid(form)
        else:
            return self.form_invalid(form)


class HoursByProjectGardenCSV(HoursByProjectMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('hours', 'project', 'recorded',)


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

from django.forms import HiddenInput, ModelForm

from floppyforms.widgets import Select

from ..forms import RecordedInput, RecordForm
from .models import HoursByGeography, HoursByTask, HoursByProject, Project


class HoursByGeographyForm(RecordForm):

    class Meta:
        model = HoursByGeography
        fields = ('hours', 'recorded_start', 'recorded', 'added_by', 'garden',)
        widgets = {
            'recorded_start': RecordedInput(),
            'recorded': RecordedInput(),
        }


class HoursByTaskForm(RecordForm):

    class Meta:
        model = HoursByTask
        fields = ('hours', 'task', 'recorded_start', 'recorded', 'added_by',
                  'garden',)
        widgets = {
            'recorded_start': RecordedInput(),
            'recorded': RecordedInput(),
        }


class AddNewProjectWidget(Select):
    template_name = 'metrics/participation/project/new_project_widget.html'


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        widgets = {
            'garden': HiddenInput(),
        }


class HoursByProjectForm(RecordForm):

    class Meta:
        model = HoursByProject
        fields = ('hours', 'project', 'recorded', 'added_by', 'garden',)
        widgets = {
            # TODO something special with gardener
            # TODO something special with project
            'project': AddNewProjectWidget(),
            'recorded': RecordedInput(),
        }

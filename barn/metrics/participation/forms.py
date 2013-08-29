from django.forms import HiddenInput, ModelForm

from floppyforms.widgets import Select

from ..harvestcount.forms import AddNewGardenerWidget
from ..harvestcount.models import Gardener
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

    def __init__(self, initial={}, *args, **kwargs):
        super(HoursByProjectForm, self).__init__(initial=initial, *args, **kwargs)
        garden = initial.get('garden', None)

        # Only get projects of this garden
        self.fields['project'].queryset = self.get_projects(garden)

        # Only get gardeners of this garden
        self.fields['gardener'].queryset = self.get_gardeners(garden)

    def get_gardeners(self, garden):
        return Gardener.objects.filter(garden=garden).order_by('name')

    def get_projects(self, garden):
        return Project.objects.filter(garden=garden).order_by('name')

    class Meta:
        model = HoursByProject
        fields = ('hours', 'project', 'gardener', 'recorded', 'added_by',
                  'garden',)
        widgets = {
            'gardener': AddNewGardenerWidget(),
            'project': AddNewProjectWidget(),
            'recorded': RecordedInput(),
        }

from django.forms import (CharField, HiddenInput, ModelChoiceField, ModelForm,
                          Textarea)
from django.utils.translation import ugettext_lazy as _

from floppyforms.widgets import Select

from farmingconcrete.models import Garden
from ..harvestcount.forms import AddNewGardenerWidget
from ..harvestcount.models import Gardener
from ..forms import RecordedField, RecordedInput, RecordForm
from .models import (HoursByGeography, HoursByTask, HoursByProject, Project,
                     ProjectHours, TaskHours)


class HoursByGeographyForm(RecordForm):
    neighborhood_definition = CharField(
        label=_('How do you define your neighborhood boundaries?'),
        help_text=_('Your zip code or cross streets are some examples of what '
                    'could go here.'),
        required=False,
        widget=Textarea,
    )
    recorded_start = RecordedField(label=_('Start date'))
    recorded = RecordedField(label=_('End date'))

    class Meta:
        model = HoursByGeography
        fields = ('neighborhood_definition', 'recorded_start', 'recorded',
                  'hours', 'photo', 'added_by', 'garden',)


class TaskHoursForm(ModelForm):
    class Meta:
        model = TaskHours


class HoursByTaskForm(RecordForm):

    class Meta:
        model = HoursByTask
        fields = ('recorded_start', 'recorded', 'added_by', 'garden',)
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


class ProjectHoursForm(ModelForm):

    garden = ModelChoiceField(
        queryset=Garden.objects.all(),
        widget=HiddenInput(),
    )

    def __init__(self, initial={}, *args, **kwargs):
        super(ProjectHoursForm, self).__init__(initial=initial, *args, **kwargs)
        garden = initial.get('garden', None)

        # Only get gardeners of this garden
        self.fields['gardener'].queryset = self.get_gardeners(garden)

    def get_gardeners(self, garden):
        return Gardener.objects.filter(garden=garden).order_by('name')

    class Meta:
        model = ProjectHours
        fields = ('record', 'gardener', 'hours', 'garden',)
        widgets = {
            'gardener': AddNewGardenerWidget(),
            'record': HiddenInput(),
        }


class HoursByProjectForm(RecordForm):

    def __init__(self, initial={}, *args, **kwargs):
        super(HoursByProjectForm, self).__init__(initial=initial, *args, **kwargs)
        garden = initial.get('garden', None)

        # Only get projects of this garden
        self.fields['project'].queryset = self.get_projects(garden)

    def get_projects(self, garden):
        return Project.objects.filter(garden=garden).order_by('name')

    class Meta:
        model = HoursByProject
        fields = ('recorded', 'project', 'added_by', 'garden',)
        widgets = {
            'project': AddNewProjectWidget(),
            'recorded': RecordedInput(),
        }

from ..forms import RecordedInput, RecordForm
from .models import HoursByGeography, HoursByTask, HoursByProject


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


class HoursByProjectForm(RecordForm):

    class Meta:
        model = HoursByProject
        fields = ('hours', 'project', 'recorded', 'added_by', 'garden',)
        widgets = {
            # TODO something special with gardener
            # TODO something special with project
            'recorded': RecordedInput(),
        }

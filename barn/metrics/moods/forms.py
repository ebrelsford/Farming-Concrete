from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from ..forms import RecordedField, RecordForm
from .models import Mood, MoodChange, MoodCount


class MoodCountForm(ModelForm):

    class Meta:
        model = MoodCount


MoodCountFormSet = inlineformset_factory(MoodChange, MoodCount,
    can_delete=False,
    extra=Mood.objects.count() * 2,
    form=MoodCountForm,
)


class MoodChangeForm(RecordForm):
    recorded_start = RecordedField(label='Start date')
    recorded = RecordedField(label='End date')

    class Meta:
        model = MoodChange
        fields = ('recorded_start', 'recorded', 'added_by', 'garden',)

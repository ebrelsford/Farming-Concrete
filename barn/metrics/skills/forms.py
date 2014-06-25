from ..forms import RecordedField, RecordForm
from .models import SmartsAndSkills


class SmartsAndSkillsForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )

    class Meta:
        model = SmartsAndSkills
        fields = ('recorded', 'participants', 'skills_shared',
                  'concepts_shared', 'projects_proposed', 'ideas_to_learn',
                  'intentions_to_collaborate', 'added_by', 'garden',)

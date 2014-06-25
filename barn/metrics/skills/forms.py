from ..forms import RecordedField, RecordForm
from .models import SmartsAndSkills


class SmartsAndSkillsForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )

    class Meta:
        model = SmartsAndSkills
        fields = (
            'recorded', 'participants',
            'skills_shared', 'skills_shared_examples',
            'concepts_shared', 'concepts_shared_examples',
            'projects_proposed', 'projects_proposed_examples',
            'ideas_to_learn', 'ideas_to_learn_examples',
            'intentions_to_collaborate', 'intentions_to_collaborate_examples',
            'added_by', 'garden',
        )

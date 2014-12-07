from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import SmartsAndSkills


class SmartsAndSkillsDatasetMixin(object):
    participants = Field(header='number of participants')
    skills_shared = Field(header='# of skills shared')
    skills_shared_examples = Field(header='examples of skills shared')
    concepts_shared = Field(header='# of concepts shared')
    concepts_shared_examples = Field(header='examples of concepts shared')
    projects_proposed = Field(header='# of projects proposed')
    projects_proposed_examples = Field(header='examples of projects proposed')
    ideas_to_learn = Field(header='# of ideas to learn')
    ideas_to_learn_examples = Field(header='examples of ideas to learn')
    intentions_to_collaborate = Field(header='# of intentions to collaborate')
    intentions_to_collaborate_examples = Field(
        header='examples of intentions to collaborate'
    )

    class Meta:
        model = SmartsAndSkills
        fields = [
            'recorded',
            'added_by_display',
            'participants',
            'skills_shared',
            'skills_shared_examples',
            'concepts_shared',
            'concepts_shared_examples',
            'projects_proposed',
            'projects_proposed_examples',
            'ideas_to_learn',
            'ideas_to_learn_examples',
            'intentions_to_collaborate',
            'intentions_to_collaborate_examples',
        ]


class SmartsAndSkillsDataset(SmartsAndSkillsDatasetMixin, MetricDatasetMixin,
                             ModelDataset):
    pass


class PublicSmartsAndSkillsDataset(SmartsAndSkillsDatasetMixin,
                                   PublicMetricDatasetMixin, ModelDataset):
    pass

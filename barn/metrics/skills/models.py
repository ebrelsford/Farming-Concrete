from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet
from ..registry import register


class SmartsAndSkillsQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'participants',
            'concepts_shared',
            'ideas_to_learn',
            'projects_proposed',
            'skills_shared',
        )
        return self.values(*values_args)


class SmartsAndSkillsManager(MetricManager):
    
    def get_queryset(self):
        return SmartsAndSkillsQuerySet(self.model)


class SmartsAndSkills(BaseMetricRecord):
    objects = SmartsAndSkillsManager()

    participants = models.IntegerField(_('number of participants'))

    skills_shared = models.IntegerField(_('# of skills shared'),
        blank=True,
        null=True,
    )
    skills_shared_examples = models.CharField(_('examples of skills shared'),
        max_length=200,
        blank=True,
        null=True,
    )

    concepts_shared = models.IntegerField(_('# of concepts shared'),
        blank=True,
        null=True,
    )
    concepts_shared_examples = models.CharField(_('examples of concepts shared'),
        max_length=200,
        blank=True,
        null=True,
    )

    projects_proposed = models.IntegerField(_('# of projects proposed'),
        blank=True,
        null=True,
    )
    projects_proposed_examples = models.CharField(_('examples of projects proposed'),
        max_length=200,
        blank=True,
        null=True,
    )

    ideas_to_learn = models.IntegerField(_('# of ideas to learn'),
        blank=True,
        null=True,
    )
    ideas_to_learn_examples = models.CharField(_('examples of ideas to learn'),
        max_length=200,
        blank=True,
        null=True,
    )

    intentions_to_collaborate = models.IntegerField(
        _('# of intentions to collaborate'),
        blank=True,
        null=True,
    )
    intentions_to_collaborate_examples = models.CharField(
        _('examples of intentions to collaborate'),
        max_length=200,
        blank=True,
        null=True,
    )


    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(SmartsAndSkills, cls).get_summarize_kwargs()
        kwargs.update({
            'participants': Sum('participants'),
            'skills_shared': Sum('skills_shared'),
            'concepts_shared': Sum('concepts_shared'),
            'projects_proposed': Sum('projects_proposed'),
            'ideas_to_learn': Sum('ideas_to_learn'),
            'intentions_to_collaborate': Sum('intentions_to_collaborate'),
        })
        return kwargs


from .export import SmartsAndSkillsDataset, PublicSmartsAndSkillsDataset


register('Skills & Knowledge in the Garden', {
    'add_record_template': 'metrics/skills/smarts/add_record.html',
    'all_gardens_url_name': 'skills_smarts_all_gardens',
    'model': SmartsAndSkills,
    'number': 4,
    'garden_detail_url_name': 'skills_smarts_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'skills_smarts_index',
    'short_name': 'smarts',
    'dataset': SmartsAndSkillsDataset,
    'public_dataset': PublicSmartsAndSkillsDataset,
    'description': _('Discovering all of the skills and knowledge within a '
                     'gardening community can help gardeners make connections '
                     'with each other and take on new projects for a stronger '
                     'garden. This report measures the number of skills, new '
                     'ideas and opportunities for collaboration within your '
                     'garden and the bigger urban agriculture community in '
                     'your city. The bottom of the report also lists some '
                     'examples of the types of skills, ideas, concepts, and '
                     'potential collaborations or projects shared during your '
                     'workshops.'),
})

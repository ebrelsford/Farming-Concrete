from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class SmartsAndSkills(BaseMetricRecord):

    participants = models.IntegerField(_('number of participants'))
    skills_shared = models.IntegerField(_('# of skills shared'))
    concepts_shared = models.IntegerField(_('# of concepts shared'))
    projects_proposed = models.IntegerField(_('# of projects proposed'))
    ideas_to_learn = models.IntegerField(_('# of ideas to learn'))
    intentions_to_collaborate = models.IntegerField(
        _('# of intentions to collaborate'),
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


register('Skills & Knowledge in the Garden', {
    'add_record_template': 'metrics/skills/smarts/add_record.html',
    'all_gardens_url_name': 'skills_smarts_all_gardens',
    'download_url_name': 'skills_smarts_garden_csv',
    'model': SmartsAndSkills,
    'number': 4,
    'garden_detail_url_name': 'skills_smarts_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'skills_smarts_index',
    'short_name': 'smarts',
    'user_gardens_url_name': 'skills_smarts_user_gardens',
})

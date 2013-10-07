from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class SmartsAndSkills(BaseMetricRecord):

    participants = models.IntegerField(_('participants'),
        help_text=_('The number of participants'),
    )

    skills_shared = models.IntegerField(_('skills shared'),
        help_text=_('The number of skills shared'),
    )

    concepts_shared = models.IntegerField(_('concepts shared'),
        help_text=_('The number of concepts shared'),
    )

    projects_proposed = models.IntegerField(_('projects proposed'),
        help_text=_('The number of projects proposed'),
    )

    ideas_to_learn = models.IntegerField(_('ideas to learn'),
        help_text=_('The number of ideas to learn'),
    )

    intentions_to_collaborate = models.IntegerField(
        _('intentions to collaborate'),
        help_text=_('The number of intentions to collaborate'),
    )

    photo = models.ImageField(_('photo'),
        help_text=_('The photo you took to record this'),
        upload_to='skills_smarts',
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


register('Smarts and Skills', {
    'all_gardens_url_name': 'skills_smarts_all_gardens',
    'model': SmartsAndSkills,
    'garden_detail_url_name': 'skills_smarts_garden_details',
    'group': 'Skills & Knowledge',
    'index_url_name': 'skills_smarts_index',
    'summarize_template': 'metrics/skills/smarts/summarize.html',
    'user_gardens_url_name': 'skills_smarts_user_gardens',
})

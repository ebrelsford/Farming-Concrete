from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register
from .export import SmartsAndSkillsDataset, PublicSmartsAndSkillsDataset
from .models import SmartsAndSkills


class SkillsConfig(AppConfig):
    label = 'skills'
    name = 'metrics.skills'

    def ready(self):
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

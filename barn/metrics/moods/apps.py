from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register


class MoodsConfig(AppConfig):
    label = 'moods'
    name = 'metrics.moods'

    def ready(self):
        from .export import MoodChangeDataset, PublicMoodChangeDataset

        register('Good Moods in the Garden', {
            'add_record_template': 'metrics/moods/change/add_record.html',
            'all_gardens_url_name': 'moods_change_all_gardens',
            'model': self.get_model('MoodChange'),
            'number': 2,
            'garden_detail_url_name': 'moods_change_garden_details',
            'group': 'Health Data',
            'group_number': 3,
            'index_url_name': 'moods_change_index',
            'short_name': 'change',
            'dataset': MoodChangeDataset,
            'public_dataset': PublicMoodChangeDataset,
            'description': _('Community gardens and green spaces are believed to '
                             'positively impact emotional wellbeing of people they '
                             'serve. They reduce stress and increase feelings of '
                             'happiness and peacefulness. In order to evaluate this '
                             'valuable quality of your garden, this report measures '
                             'all of the good and bad moods people registered as they '
                             'walked in and out of your garden in a particular '
                             'period. The following results will help you understand '
                             'your garden\'s emotional value and might also lead to '
                             'different ways to make your space have an increased '
                             'positive impact on participants and visitors.'),
        })

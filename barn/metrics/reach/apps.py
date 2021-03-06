from django.utils.translation import ugettext_lazy as _

from ..apps import MetricConfig
from ..registry import register


class ReachConfig(MetricConfig):
    label = 'reach'
    name = 'metrics.reach'

    def get_metric_models(self):
        return [self.get_model(c) for c in ('ProgramReach',)]

    def ready(self):
        super(ReachConfig, self).ready()

        from .export import ProgramReachDataset, PublicProgramReachDataset

        register('Reach of Programs', {
            'all_gardens_url_name': 'reach_program_all_gardens',
            'model': self.get_model('ProgramReach'),
            'number': 5,
            'garden_detail_url_name': 'reach_program_garden_details',
            'group': 'Social Data',
            'group_number': 2,
            'index_url_name': 'reach_program_index',
            'short_name': 'program',
            'dataset': ProgramReachDataset,
            'public_dataset': PublicProgramReachDataset,
            'description': _('This report displays the number of people who attended '
                             'the various programs offered in your garden during a '
                             'specified time period. The report also references the '
                             'age, gender, and geographic location of attendees, as '
                             'well as the nature of the program.'),
        })

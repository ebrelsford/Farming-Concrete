from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from ..registry import register
from .export import (HoursByGeographyDataset, PublicHoursByGeographyDataset,
                     HoursByProjectDataset, PublicHoursByProjectDataset,
                     HoursByTaskDataset, PublicHoursByTaskDataset)
from .models import HoursByGeography, HoursByProject, HoursByTask


class ParticipationConfig(AppConfig):
    label = 'participation'
    name = 'metrics.participation'

    def ready(self):
        register('Participation by Geography', {
            'add_record_label': 'Add participation hours',
            'add_record_template': 'metrics/participation/geography/add_record.html',
            'all_gardens_url_name': 'participation_geography_all_gardens',
            'model': HoursByGeography,
            'number': 1,
            'garden_detail_url_name': 'participation_geography_garden_details',
            'group': 'Social Data',
            'group_number': 2,
            'index_url_name': 'participation_geography_index',
            'short_name': 'geography',
            'dataset': HoursByGeographyDataset,
            'public_dataset': PublicHoursByGeographyDataset,
            'description': _('Community gardens are created, maintained and managed '
                             'by local volunteers who trade hours of service for '
                             'access to the garden. The following report quantifies '
                             'the total hours volunteers worked in your garden for '
                             'your specified time period. The top graph shows the '
                             'number of hours worked by volunteers in your '
                             'neighborhood, and the bottom graph depicts hours worked '
                             'by volunteers from outside of your neighborhood.'),
        })


        register('Participation by Task', {
            'add_record_label': 'Add participation hours',
            'add_record_template': 'metrics/participation/task/add_record.html',
            'all_gardens_url_name': 'participation_task_all_gardens',
            'model': HoursByTask,
            'number': 2,
            'garden_detail_url_name': 'participation_task_garden_details',
            'group': 'Social Data',
            'group_number': 2,
            'index_url_name': 'participation_task_index',
            'short_name': 'task',
            'dataset': HoursByTaskDataset,
            'public_dataset': PublicHoursByTaskDataset,
            'description': _('Every garden and farm has an ongoing list of tasks that '
                             'need to be completed - weeding, planting, making '
                             'repairs etc. Depending on the season, gardens and farms '
                             'require a certain amount of time for each particular '
                             'task; hence it becomes important to track and manage '
                             'the hours spent on each task activity. This report '
                             'measures the number of volunteer hours per task.'),
        })


        register('Participation by Project', {
            'add_record_label': 'Add participation hours',
            'add_record_template': 'metrics/participation/project/add_record.html',
            'all_gardens_url_name': 'participation_project_all_gardens',
            'model': HoursByProject,
            'number': 3,
            'garden_detail_url_name': 'participation_project_garden_details',
            'group': 'Social Data',
            'group_number': 2,
            'index_url_name': 'participation_project_index',
            'short_name': 'project',
            'dataset': HoursByProjectDataset,
            'public_dataset': PublicHoursByProjectDataset,
            'description': _('Occasionally gardens and farms undertake special '
                             'projects like building a fence or painting a mural. '
                             'These projects are different from daily garden tasks '
                             'and may require additional participation. This report '
                             'measures the total hours spent by volunteers to '
                             'complete big projects in your garden.'),
        })

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template

from ..models import HoursByGeography

register = template.Library()


class GardenerProjectHours(AsTag):
    options = Options(
        Argument('gardener', resolve=True, required=True),
        'for',
        Argument('hours_by_project', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, gardener, hours_by_project):
        return hours_by_project[gardener.name]


class TaskHours(AsTag):
    options = Options(
        Argument('task', resolve=True, required=True),
        'for',
        Argument('hours_by_task', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, task, hours_by_task):
        return hours_by_task[task.name]


class GardenPhotos(AsTag):
    options = Options(
        'for',
        Argument('garden', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        return [r.photo for r in HoursByGeography.objects.filter(garden=garden) if r.photo]


register.tag(GardenPhotos)
register.tag(GardenerProjectHours)
register.tag(TaskHours)

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template

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


register.tag(GardenerProjectHours)
register.tag(TaskHours)

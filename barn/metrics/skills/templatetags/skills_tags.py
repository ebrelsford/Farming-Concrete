from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template

from ..models import SmartsAndSkills

register = template.Library()


class GardenPhotos(AsTag):
    options = Options(
        'for',
        Argument('garden', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        return [r.photo for r in SmartsAndSkills.objects.filter(garden=garden) if r.photo]


register.tag(GardenPhotos)

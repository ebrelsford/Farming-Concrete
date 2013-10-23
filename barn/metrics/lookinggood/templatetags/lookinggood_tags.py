from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template

from ..models import LookingGoodPhoto

register = template.Library()


class GardenPhotos(AsTag):
    options = Options(
        'for',
        Argument('garden', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        p = LookingGoodPhoto.objects.filter(event__garden=garden)
        print "PHOTOSSS", p.count()
        return p


register.tag(GardenPhotos)

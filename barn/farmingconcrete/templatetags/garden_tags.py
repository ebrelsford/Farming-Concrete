from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag

from accounts.utils import get_profile

register = template.Library()

from ..utils import garden_type_label


class GardenList(InclusionTag):
    options = Options(
        Argument('user'),
    )
    template = 'farmingconcrete/garden_list.html'

    def get_gardens(self, user):
        try:
            if user.is_authenticated():
                profile = get_profile(user)
                return profile.gardens.all().order_by('name')
        except Exception:
            return []

    def get_context(self, context, user):
        context.update({
            'gardens': self.get_gardens(user),
        })
        return context


register.filter('garden_type_label', garden_type_label)
register.tag(GardenList)

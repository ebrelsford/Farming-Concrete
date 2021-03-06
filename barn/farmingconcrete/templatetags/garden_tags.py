from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag

from accounts.utils import get_profile

register = template.Library()


class GardenList(InclusionTag):
    options = Options(
        Argument('user'),
        Argument('template', required=False, resolve=False),
    )
    template = 'farmingconcrete/garden_list.html'

    def get_gardens(self, user):
        try:
            if user.is_authenticated():
                profile = get_profile(user)
                return profile.gardens.all().order_by('name')
        except Exception:
            return []

    def get_context(self, context, user, template):
        context.update({
            'gardens': self.get_gardens(user),
        })
        return context

    def get_template(self, context, **kwargs):
        default_template = super(GardenList, self).get_template(context, **kwargs)
        return kwargs.get('template', None) or default_template


class GardenMemberList(InclusionTag):
    options = Options(
        Argument('garden'),
    )
    template = 'farmingconcrete/garden_member_list.html'

    def get_garden_members(self, garden):
        if garden:
            return garden.gardenmembership_set.all()
        return []

    def get_context(self, context, garden):
        context.update({
            'members': self.get_garden_members(garden),
        })
        return context


register.tag(GardenList)
register.tag(GardenMemberList)

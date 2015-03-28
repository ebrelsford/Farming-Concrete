from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag

from accounts.models import GardenGroupUserMembership

register = template.Library()


class GardenGroupList(InclusionTag):
    options = Options(
        Argument('user'),
        Argument('template', required=False, resolve=False),
    )
    template = 'farmingconcrete/gardengroup_list.html'

    def get_groups(self, user):
        return [m.group for m in GardenGroupUserMembership.objects.filter(
            is_admin=True,
            user_profile__user=user,
        )]

    def get_context(self, context, user, template):
        context.update({
            'groups': self.get_groups(user),
        })
        return context

    def get_template(self, context, **kwargs):
        default_template = super(GardenGroupList, self).get_template(context, **kwargs)
        return kwargs.get('template', None) or default_template


register.tag(GardenGroupList)

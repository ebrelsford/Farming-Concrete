from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag

from accounts.models import GardenGroupUserMembership
from ..models import GardenGroupMembership

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


class GardenGroupInviteList(InclusionTag):
    options = Options(
        Argument('garden'),
        Argument('template', required=False, resolve=False),
    )
    template = 'farmingconcrete/gardengroup/invite_list.html'

    def get_group_memberships(self, garden):
        return GardenGroupMembership.by_status.pending_invited().filter(
            garden=garden,
        )

    def get_context(self, context, garden, template):
        context.update({
            'group_memberships': self.get_group_memberships(garden),
        })
        return context

    def get_template(self, context, **kwargs):
        default_template = super(GardenGroupInviteList, self).get_template(context, **kwargs)
        return kwargs.get('template', None) or default_template


class GardenGroupInviteCount(AsTag):
    options = Options(
        Argument('garden'),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, garden):
        return GardenGroupMembership.by_status.pending_invited().filter(
            garden=garden,
        ).count()


class GardenGroupMemberList(InclusionTag):
    options = Options(
        Argument('group'),
    )
    template = 'farmingconcrete/gardengroup/member_list.html'

    def get_garden_group_members(self, group):
        if group:
            return group.members()
        return []

    def get_context(self, context, group):
        context.update({
            'members': self.get_garden_group_members(group),
        })
        return context


register.tag(GardenGroupList)
register.tag(GardenGroupInviteCount)
register.tag(GardenGroupInviteList)
register.tag(GardenGroupMemberList)

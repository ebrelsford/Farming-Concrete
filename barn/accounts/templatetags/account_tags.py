from django import template

from classytags.arguments import Argument
from classytags.core import Options, Tag

register = template.Library()


class IfGardenAdmin(Tag):
    name = 'ifgardenadmin'
    options = Options(
        Argument('garden'),
        blocks=[('endifgardenadmin', 'nodelist')],
    )

    def render_tag(self, context, garden, nodelist):
        user = context['user']
        # If user is a garden admin for this garden OR can edit any garden
        if garden.is_admin(user):
            return nodelist.render(context)
        return ''


class IfGardenGroupAdmin(Tag):
    name = 'ifgardengroupadmin'
    options = Options(
        Argument('gardengroup'),
        blocks=[('endifgardengroupadmin', 'nodelist')],
    )

    def render_tag(self, context, gardengroup, nodelist):
        user = context['user']
        if (user.has_perm('farmingconcrete.can_edit_any_garden') or
            gardengroup.is_admin(user)):
            return nodelist.render(context)
        return ''


register.tag(IfGardenAdmin)
register.tag(IfGardenGroupAdmin)

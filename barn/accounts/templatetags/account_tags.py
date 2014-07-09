from django import template

from classytags.arguments import Argument
from classytags.core import Options, Tag

from ..utils import is_admin

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
        if is_admin(user, garden):
            return nodelist.render(context)
        return ''


register.tag(IfGardenAdmin)

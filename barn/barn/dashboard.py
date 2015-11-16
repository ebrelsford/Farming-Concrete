"""
This file was generated with the customdashboard management command.
"""

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):

    def init_with_context(self, context):
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

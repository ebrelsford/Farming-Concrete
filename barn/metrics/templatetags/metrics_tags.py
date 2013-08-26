from django import template
from django.template.loader import render_to_string

from classytags.arguments import Argument
from classytags.core import Options, Tag

from ..registry import registry

register = template.Library()


class Summarize(Tag):
    options = Options(
        Argument('name'),
        Argument('summary'),
    )

    def render_tag(self, context, name, summary):
        return render_to_string(self.get_template(name), summary)

    def get_template(self, metric_name):
        try:
            template_name = registry[metric_name]['summarize_template']
        except Exception:
            app_label = registry[metric_name]['model']._meta.app_label
            template_name = 'metrics/%s/summarize.html' % app_label
        return template_name


register.tag(Summarize)

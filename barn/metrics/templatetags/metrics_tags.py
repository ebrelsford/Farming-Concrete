from django import template
from django.template.loader import render_to_string

from classytags.arguments import Argument
from classytags.core import Options, Tag


register = template.Library()


class Summarize(Tag):
    options = Options(
        Argument('app'),
        Argument('summary'),
    )

    def render_tag(self, context, app, summary):
        return render_to_string(self.get_template(app), summary)

    def get_template(self, metric_name):
        return 'metrics/%s/summarize.html' % metric_name


register.tag(Summarize)

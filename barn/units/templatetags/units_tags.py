from django import template

from .. import convert


register = template.Library()


@register.assignment_tag
def to_preferred_weight_units(value, gardens):
    if not value or value == '':
        return None
    return convert.to_preferred_weight_units(value, gardens)

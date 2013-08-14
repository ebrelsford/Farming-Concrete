from django import template

register = template.Library()


@register.filter
def garden_type_label(garden_type):
    if garden_type and garden_type != 'all':
        return '%ss' % garden_type
    return ''

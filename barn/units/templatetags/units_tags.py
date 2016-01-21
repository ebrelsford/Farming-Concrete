from django import template

from .. import convert


register = template.Library()


@register.assignment_tag
def preferred_distance_units(gardens):
    return convert.preferred_distance_units(gardens)


@register.assignment_tag
def to_preferred_volume_units_from_cubic_meters(value, gardens):
    if not value or value == '':
        return None
    return convert.to_preferred_volume_units(gardens, cubic_meters=value)


@register.assignment_tag
def to_preferred_volume_units_from_liters(value, gardens):
    if not value or value == '':
        return None
    return convert.to_preferred_volume_units(gardens, liters=value)


@register.assignment_tag
def to_preferred_weight_units(value, gardens):
    if not value or value == '':
        return None
    return convert.to_preferred_weight_units(value, gardens)

from django import template

register = template.Library()

from ..utils import garden_type_label


register.filter('garden_type_label', garden_type_label)

from django import template

register = template.Library()

def get(d, key):
    """Get a key from a dict"""
    return d.get(key, '')

register.filter(get)

from django import template

from modules.utils import *

register = template.Library()

@register.filter('isk')
def isk(value):
    parts = str(value).split('.')
    classes = splitN(3, reverseStr(parts[0]))
    classes = list(map(reverseStr, classes))
    classes.reverse()
    parts[0] = '.'.join(classes)
    return ','.join(parts)

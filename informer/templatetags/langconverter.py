from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def langconverter(path, lang):
    spath = str(path)
    result = '/'+lang+spath[3:len(spath)-1]
    return result

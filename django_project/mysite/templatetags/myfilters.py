from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})

from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})
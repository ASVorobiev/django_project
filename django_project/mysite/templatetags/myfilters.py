from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='week_dates')
def week_dates(value, arg):
    # day = '12/Oct/2013'
    # dt = datetime.strptime(day, '%d/%b/%Y')
    dt = datetime.now()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    print(start)
    print(end)
    print(start.strftime('%d/%b/%Y'))
    print(end.strftime('%d/%b/%Y'))


    return value.as_widget(attrs={'class': arg})
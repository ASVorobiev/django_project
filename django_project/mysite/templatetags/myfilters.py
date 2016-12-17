from django import template
from django.utils.timesince import timesince
from datetime import datetime

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def partition(thelist, n):
    """
    Break a list into ``n`` pieces. The last list may be larger than the rest if
    the list doesn't break cleanly. That is::
        >>> l = range(10)
        >>> partition(l, 2)
        [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        >>> partition(l, 3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]
        >>> partition(l, 4)
        [[0, 1], [2, 3], [4, 5], [6, 7, 8, 9]]
        >>> partition(l, 5)
        [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    p = len(thelist) / n
    return [thelist[p * i:p * (i + 1)] for i in range(n - 1)] + [thelist[p * (i + 1):]]


@register.filter
def partition_horizontal(thelist, n):
    """
    Break a list into ``n`` peices, but "horizontally." That is,
    ``partition_horizontal(range(10), 3)`` gives::

        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9],
         [10]]

    Clear as mud?
    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    newlists = [list() for i in range(n)]
    for i, val in enumerate(thelist):
        newlists[i % n].append(val)
    return newlists


@register.filter
def split_by_three(data):
    return [data[i:i+3] for i in range(0, len(data), 3)]


@register.filter
def timedelta(value, arg=None):
    if not value:
        return ''
    else:
        value = datetime.combine(value.start_date, value.start_time)
    if arg:
        cmp = arg
    else:
        cmp = datetime.now()
    if value > cmp:
        return "через %s" % timesince(cmp, value)
    else:
        return "%s назад" % timesince(value, cmp)
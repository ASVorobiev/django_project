import json
from datetime import date, timedelta
from time import sleep

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from django_project.mysite.forms import AddNewEvent
from django_project.mysite.models import Events, Locations
from transliterate import translit
from digg_paginator import DiggPaginator

today = date.today()


# Create your views here.


def home(request):
    return events_list(request)


def paginator(request, events):
    paginator = Paginator(events, 10)  # Show 25 events per page
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return paginator.page(paginator.num_pages)

def events_list(request, site_screen_name=None):
    all_events = Events.objects.exclude(start_date__lte=today).exclude(
        start_date__gte=today + timedelta(days=45)).order_by('start_date')
    priority_events = Events.objects.exclude(start_date__lte=today).order_by('-priority', 'start_date')[:10]
    locations = Locations.objects.all()

    if site_screen_name:
        location = Locations.objects.get(site_screen_name=site_screen_name)
        location_id = location.id
        location_events = Events.objects.filter(location=location_id).exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=45)).order_by('priority').order_by('start_date')
        priority_events = Events.objects.filter(location=location_id).exclude(
            start_date__lte=today).order_by('-priority', 'start_date')[:10]
        current_location = Locations.objects.get(id=location_id)

        return render(request, 'mysite/events_list.html', {'location_events': paginator(request, location_events),
                                                           'priority_events': priority_events,
                                                           'locations': locations,
                                                           'current_location': current_location,
                                                           })
    else:
        current_location = 'Выберите ваш город'
        return render(request, 'mysite/events_list.html', {'location_events': paginator(request, all_events),
                                                           'locations': locations,
                                                           'priority_events': priority_events,
                                                           'current_location': current_location})


def events_details(request, site_screen_name, pk):
    locations = Locations.objects.all()
    current_location = Locations.objects.get(site_screen_name=site_screen_name)
    event_data = Events.objects.get(id=pk)
    return render(request, 'mysite/event_details.html', {'event_data': event_data,
                                                         'current_location': current_location,
                                                         'locations': locations,
                                                         'title_translit': 'text'})


def add_event_form(request):
    if request.user.is_anonymous():
        request.session['add_event_form_http_referer'] = 1
        return redirect('login',)
    context = {}
    context['EventsMod'] = AddNewEvent
    context.update(csrf(request))
    if request.POST:
        new_event = AddNewEvent(request.POST, request.FILES)
        new_event.title = request.POST['title']
        new_event.description = request.POST['description']
        new_event.location = request.POST['location']
        new_event.image = request.FILES['image']
        new_event.start_time = request.POST['start_time']
        new_event.start_date = request.POST['start_date']
        res = new_event.save()
        return redirect('event_details', location_id=res.location.id, pk=res.pk)
    return render(request, 'mysite/add_event_form.html', context)
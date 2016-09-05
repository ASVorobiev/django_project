from random import shuffle

from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from mysite.forms import AddNewEvent
from mysite.models import UploadForm, Upload, Events, Locations
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# Create your views here.


def home(request):
    return events_list(request)


def events_list(request, location_id=None):
    all_events = Events.objects.all().order_by('-start_date')[:28]
    priority_events = Events.objects.filter(priority=1).order_by('-start_date')[:10]
    locations = Locations.objects.all()

    if location_id:
        location_events = Events.objects.filter(location=location_id).order_by('-id')[:28]
        current_location = Locations.objects.get(id=location_id)
        return render(request, 'mysite/events_list.html', {'location_events': location_events,
                                                           'priority_events': priority_events,
                                                           'locations': locations,
                                                           'current_location': current_location})
    else:
        current_location = 'Выберите ваш город'
        return render(request, 'mysite/events_list.html', {'location_events': all_events,
                                                           'locations': locations,
                                                           'priority_events': priority_events,
                                                           'current_location': current_location})


def events_details(request, location_id, pk):
    event_data = Events.objects.get(id=pk)
    current_location = Locations.objects.get(id=location_id)
    locations = Locations.objects.all()
    return render(request, 'mysite/event_details.html', {'event_data': event_data,
                                                         'current_location': current_location,
                                                         'locations': locations})


def add_event_form(request):
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

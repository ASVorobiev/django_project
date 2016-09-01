from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from mysite.forms import AddNewEvent
from mysite.models import UploadForm, Upload, Events
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.


def home(request):
    if request.method == "POST":
        img = UploadForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
            return HttpResponseRedirect(reverse('imageupload'))
    else:
        img=UploadForm()
    images=Upload.objects.all()
    return render(request, 'home.html', {'form':img, 'images':images})


def events_list(request):
    posts = Events.objects.all()
    return render(request, 'mysite/events_list.html', {'posts': posts})

def add_event_form(request):
    #posts = AddNewEvent
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
        new_event.save()
        return redirect('post_list')
    return render(request, 'mysite/add_event_form.html', context)
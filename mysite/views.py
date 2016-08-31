from django.shortcuts import render
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
    posts = Events.objects.all()
    return render(request, 'mysite/add_event_form.html', {'posts': posts})
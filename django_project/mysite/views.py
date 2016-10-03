import copy
import hashlib
import json
import os
from datetime import date, timedelta
from io import BytesIO


from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles import finders

from django_project.mysite.forms import AddNewEvent
from django_project.mysite.models import Events, Locations, MysiteOrganizers
from transliterate import translit

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps

today = date.today()


def home(request):
    return events_list(request)


def events_list(request, site_screen_name=None):

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

        return render(request, 'mysite/events_list.html', {'location_events': location_events,
                                                           'priority_events': priority_events,
                                                           'locations': locations,
                                                           'current_location': current_location,
                                                           })
    else:
        all_events = Events.objects.exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=45)).order_by('start_date')
        current_location = 'Выберите ваш город'
        return render(request, 'mysite/events_list.html', {'location_events': all_events,
                                                           'locations': locations,
                                                           'priority_events': priority_events,
                                                           'current_location': current_location})


def events_details(request, site_screen_name, pk, title_translit='dont_remove'):
    locations = Locations.objects.all()
    current_location = Locations.objects.get(site_screen_name=site_screen_name)
    event_data = Events.objects.get(id=pk)
    events_from_this_organizator = Events.objects.filter(location=event_data.location_id, organizer=event_data.organizer_id).exclude(id=event_data.id).exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=45)).order_by('priority').order_by('start_date')
    events_from_this_place = Events.objects.filter(location=event_data.location_id, organizer=event_data.place_id).exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=45)).order_by('priority').order_by('start_date')
    return render(request, 'mysite/event_details.html', {'event_data': event_data,
                                                         'events_from_this_organizator': events_from_this_organizator,
                                                         'events_from_this_place': events_from_this_place,
                                                         'current_location': current_location,
                                                         'locations': locations,
                                                         'title_translit': translit(event_data.title, 'ru',
                                                                                    reversed=True).replace(' ', '_')
                                                         })


def pill(image_io):
    im = Image.open(image_io)
    logo = Image.open(finders.find('logo/vkalendare_logo_only.png'))
    new_text = 'Информационная поддержка: "Афиша вКалендаре". Ещё больше мероприятий: www.vkalendare.com'

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.load_default()
    (width, height) = im.size
    p_height = int(height * 0.05)
    ltrb_border = (0, 0, 0, p_height)
    im_with_border = ImageOps.expand(im, border=ltrb_border, fill='black')

    print('border size:', width, p_height)

    logo_size = int(p_height * 0.8), int(p_height * 0.8)
    logo.thumbnail(logo_size, Image.ANTIALIAS)

    ttf = finders.find('fonts/roboto/Roboto-Regular.ttf')
    font = ImageFont.truetype(ttf, int(height * 0.025))
    if font.getsize(new_text)[0] > (width*0.9):
        q = width / font.getsize(new_text)[0]
        print(q)
        font = ImageFont.truetype(ttf, int(height * 0.022 * q))

    draw = ImageDraw.Draw(im_with_border)
    print(font.getsize(new_text))
    draw.text((width * 0.01 + p_height, height + (p_height / 2 - font.getsize(new_text)[1] / 2)), new_text,
              fill='white', font=font)

    im_with_border.paste(logo.convert('RGB'), (int(width * 0.01), int(height + p_height * 0.1)), logo)

    max_size = 1920, 1080
    buffer = BytesIO()
    im_with_border.thumbnail(max_size, Image.ANTIALIAS)
    im_with_border.save(fp=buffer, format='JPEG')

    img = buffer.getvalue()

    size = 128, 128
    im.thumbnail(size, Image.ANTIALIAS)
    buffer2 = BytesIO()
    im.save(buffer2, "JPEG")
    thumb = buffer2.getvalue()
    return ContentFile(img), ContentFile(thumb)


def add_event_form(request):
    if request.user.is_anonymous():
        request.session['add_event_form_http_referer'] = 1
        return redirect('login',)
    context = {}
    context['form'] = AddNewEvent(request.POST, request.FILES)
    context['locations'] = Locations.objects.all()
    context.update(csrf(request))
    if request.POST:

        p = pill(request.FILES['image'])
        img_file = InMemoryUploadedFile(p[0], None, 'poster.jpg', 'image/jpeg', p[0].tell, None)
        thumb_file = InMemoryUploadedFile(p[1], None, 'thumb.jpg', 'image/jpeg', p[1].tell, None)
        request.FILES['image'] = img_file
        request.FILES['thumb'] = thumb_file

        new_event = AddNewEvent(request.POST, request.FILES)
        if new_event.is_valid():
            new_event.title = request.POST['title']
            new_event.description = request.POST['description']
            new_event.location = request.POST['location']
            new_event.start_time = request.POST['start_time']
            new_event.start_date = request.POST['start_date']
            new_event.image = request.FILES['image']
            new_event.thumb = request.FILES['thumb']
            # res = new_event.save()
            context['form'] = new_event
            if new_event.is_valid():
                res = new_event.save(commit=False)
                res.owner = request.user
                note = res.save()
                return redirect('event_details', site_screen_name=res.location.site_screen_name, pk=res.pk, title_translit='new')
    return render_to_response('mysite/add_event_form.html', context, context_instance=RequestContext(request))
    # return render(request, 'mysite/add_event_form.html', context)


def admin_list(request):
    if request.method == "POST":
        if request.POST['task'] == 'set_active':
            event = Events.objects.get(pk=request.POST['event_id'])
            event.is_active = 1
            event.save()
            return HttpResponse(json.dumps({'error_code': 0}), content_type='application/json')

        if request.POST['task'] == 'set_active_with_priority':
            event = Events.objects.get(pk=request.POST['event_id'])
            event.is_active = 1
            event.priority = 1
            event.save()
            return HttpResponse(json.dumps({'error_code': 0}), content_type='application/json')

        if request.POST['task'] == 'set_dismiss':
            event = Events.objects.get(pk=request.POST['event_id'])
            event.is_active = 0
            event.save()
            return HttpResponse(json.dumps({'error_code': 0}), content_type='application/json')

        context = {'unique': '0.00', 'seo_check': {'count_chars_with_space': 110, 'mixed_words': [], 'spam_percent': 22, 'list_keys': [{'count': 2, 'key_title': 'друг'}], 'count_words': 15, 'count_chars_without_space': 96, 'water_percent': 16, 'list_keys_group': [{'count': 2, 'sub_keys': [], 'key_title': 'друг'}]}, 'text_unique': '0.00', 'spell_check': [], 'result_json': {'clear_text': 'На основе одного шаблона генерируется множество статей с невысокой уникальностью очень похожих друг на друга', 'urls': [{'url': 'http://vk.com/wall-91072377', 'plagiat': 100, 'words': '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14'}, {'url': 'http://pr-cy.ru/lib/seo/Kontent-sayta-SEO-kopirayting-Unikal-nost-kontenta', 'plagiat': 100, 'words': '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14'}], 'unique': 0, 'mixed_words': '', 'date_check': '19.09.2016 19:58:30'}, 'text_uid': '57e0192d87fb8'}
        return HttpResponse(json.dumps(context), content_type='application/json')

def jdata(request):
    if request.method == "POST":
        if request.POST['task'] == 'get_location_places':
            places = MysiteOrganizers.objects.raw("SELECT * from mysite_organizers where id in (SELECT DISTINCT organizer_id from mysite_events WHERE location_id = 1) AND confidence > 1 AND vk_type = 'group' ORDER BY followers")
            # places = Events.objects.get(pk=request.POST['location_id'])
            return HttpResponse(json.dumps({'location_places': places}), content_type='application/json')
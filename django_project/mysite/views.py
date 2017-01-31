# -*- coding: utf-8 -*-
import copy
import hashlib
import json
import os
from datetime import date, timedelta, timezone

import subprocess

from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from io import BytesIO
import random
import sys

import re
from time import sleep

import nltk
import requests
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django_project.mysite.forms import AddNewEvent, CustomPlacesForm, ConfidenceNewEvent
from django_project.mysite.models import Events, Locations, MysiteOrganizers, MysiteCategories, TaggedCategories, \
    Customplaces, MysiteVkEvents, LocationCities
from transliterate import translit
from django.template.defaulttags import register

from datetime import datetime, timedelta
import tzlocal
import pytz
from tzlocal import get_localzone

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps

import pymorphy2
import logging

logger = logging.getLogger(__name__)
today = date.today()


def home(request):
    return events_list(request)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def events_list(request, site_screen_name=None):
    response = {}
    response['locations'] = Locations.objects.exclude(created=0, is_deleted=1).order_by('name').all()

    if not request.user.is_anonymous and not site_screen_name and request.user.location_id:
        location = Locations.objects.get(pk=request.user.location_id)
        site_screen_name = location.site_screen_name
    elif 'user_location' in request.session and not site_screen_name:
        location = Locations.objects.get(pk=request.session['user_location'])
        site_screen_name = location.site_screen_name
        request.user.location = location
    elif 'user_location' in request.session and request.user.is_anonymous:
        location = Locations.objects.get(pk=request.session['user_location'])
        request.user.location = location

    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')
    if 'free' in request.GET:
        free = True
    else:
        free = False
    from_date = request.GET.get('from_date', '')  # 2015-01-09
    to_date = request.GET.get('to_date', '')
    place = request.GET.get('place', '')

    response['location_events'] = Events.objects.all().order_by('-priority', 'start_date').filter(is_active=1,
                                                                                                  is_deleted=0)

    category_obj = {}
    response['priority_events'] = response['location_events'].filter(start_date__gt=today).order_by('?')
    if site_screen_name:
        location = Locations.objects.exclude(created=0, is_deleted=1).get(site_screen_name=site_screen_name)
        location_id = location.id
        response['location_events'] = response['location_events'].filter(location__id=location_id)

        response['priority_events'] = response['priority_events'].filter(location=location_id)
        response['current_location'] = Locations.objects.get(id=location_id)
        response['vk_group_id'] = response['current_location'].vk_group_id

        for ctgory in MysiteCategories.objects.all():
            category_events = Events.objects.filter(location__id=location_id, is_deleted=0,
                                                    start_date__gte=today, start_date__lte=today + timedelta(days=45),
                                                    tag_it__id__in=ctgory.taggedcategories_set.values('tag_id'))
            # category_events = location_events.filter(tag_it__id__in=ctgory.taggedcategories_set.values('tag_id'))
            if category_events:
                category_obj[ctgory.name.capitalize()] = {'count': len(category_events)}

        response['need_location'] = False
    else:
        response['current_location'] = ''
        response['need_location'] = True

    response['priority_events'] = response['priority_events'][:8]
    response['categories'] = category_obj

    if category:
        response['location_events'] = response['location_events'].filter(tag_it__id__in=TaggedCategories.objects.filter(
            category_id__name=category).values('tag_id'))
    if tag:
        response['location_events'] = response['location_events'].filter(tag_it__name=tag)
    if free:
        response['location_events'] = response['location_events'].filter(is_free=1)
    if place:
        place_obj = Customplaces.objects.get(id=place)
        response['location_events'] = response['location_events'].filter(Q(organizer=place_obj.org_parent_id) | Q(place=place_obj.id))
    if from_date or to_date:
        if from_date:
            response['location_events'] = response['location_events'].filter(start_date__gte=from_date)
        if to_date:
            response['location_events'] = response['location_events'].filter(start_date__lte=to_date)
    else:
        response['location_events'] = response['location_events'].filter(start_date__gte=today,
                                                                         start_date__lte=today + timedelta(days=45))

    dt = datetime.now()
    start = dt - timedelta(days=dt.weekday())
    response['start_week_date'] = str(start.date())
    response['start_weekend_date'] = str((start + timedelta(days=5)).date())
    response['end_week_date'] = str((start + timedelta(days=6)).date())

    meropriyatie = pymorphy2.MorphAnalyzer().parse('мероприятие')[0]
    response['this_week_event_count'] = len(
        response['location_events'].filter(start_date__gte=response['start_week_date'],
                                           start_date__lte=response['end_week_date']))
    if response['this_week_event_count']:
        response['this_week_event_count'] = "%s %s" % (response['this_week_event_count'], meropriyatie.make_agree_with_number(response['this_week_event_count']).word)
    else:
        response['this_week_event_count'] = 'мероприятий не найдено'

    response['this_weekend_event_count'] = len(
        response['location_events'].filter(start_date__gte=response['start_weekend_date'],
                                           start_date__lte=response['end_week_date']))
    if response['this_weekend_event_count']:
        response['this_weekend_event_count'] = "%s %s" % (response['this_weekend_event_count'], meropriyatie.make_agree_with_number(response['this_weekend_event_count']).word)
    else:
        response['this_weekend_event_count'] = 'мероприятий не найдено'

    response['free_event_count'] = len(response['location_events'].filter(is_free=1))
    if response['free_event_count']:
        response['free_event_count'] = "%s %s" % (response['free_event_count'], meropriyatie.make_agree_with_number(response['free_event_count']).word)
    else:
        response['free_event_count'] = 'мероприятий не найдено'

    return render(request, 'mysite/events_list.html', response)


def events_details(request, site_screen_name, pk, title_translit='dont_remove'):
    locations = Locations.objects.exclude(created=0, is_deleted=1).order_by('name').all()
    current_location = Locations.objects.get(site_screen_name=site_screen_name)
    event_data = Events.objects.get(id=pk)
    events_from_this_organizator = Events.objects.filter(location=event_data.location_id,
                                                         organizer=event_data.organizer_id).exclude(
        id=event_data.id).exclude(start_date__lte=today).exclude(
        start_date__gte=today + timedelta(days=45)).order_by('priority').order_by('start_date')
    events_from_this_place = Events.objects.filter(location=event_data.location_id,
                                                   organizer=event_data.place_id).exclude(
        start_date__lte=today).exclude(
        start_date__gte=today + timedelta(days=45)).order_by('priority').order_by('start_date')
    return render(request, 'mysite/event_details.html', {'event_data': event_data,
                                                         'events_from_this_organizator': events_from_this_organizator,
                                                         'events_from_this_place': events_from_this_place,
                                                         'current_location': current_location,
                                                         'locations': locations,
                                                         'event_tags': event_data.tag_it.names(),
                                                         'title_translit': translit(event_data.title, 'ru',
                                                                                    reversed=True).replace(' ', '_')
                                                         })


def pill(image_io, image_logo='logo/vkalendare_logo_only.png'):
    im = Image.open(image_io)
    logo = Image.open(finders.find(image_logo))
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
    if font.getsize(new_text)[0] > (width * 0.9):
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
    im_with_border.save(fp=buffer, format='JPEG', optimize=True, quality=75)

    img = buffer.getvalue()

    size = 128, 128
    im.thumbnail(size, Image.ANTIALIAS)
    buffer2 = BytesIO()
    im.save(buffer2, "JPEG", optimize=True, quality=75)
    thumb = buffer2.getvalue()
    return ContentFile(img), ContentFile(thumb)


@csrf_exempt
def add_event_selector(request):
    if request.user.is_anonymous():
        request.session['add_event_selector_http_referer'] = 1
        return redirect('login', )
    if request.POST:
        if request.POST['event_has'] == 'yes':
            if 'vk.com/event' in request.POST['vk_event_url']:
                event_id = int(request.POST['vk_event_url'].split('vk.com/event')[1])
                event_screen_name = event_id
            else:
                event_screen_name = request.POST['vk_event_url'].split('/')[-1]

            url = 'https://api.vk.com/method/groups.getById'
            resp = requests.post(url, data={'group_id': event_screen_name,
                                            'fields': 'city',
                                            'version': '5.62'}).json()
            if 'response' in resp:
                try:
                    if resp['response'][0]['type'] == "event":
                        event_id = resp['response'][0]['gid']
                        print(event_id)
                    elif resp['response'][0]['type'] == "group":
                        messages.add_message(request, messages.INFO, 'Вы пытаетесь добавить ГРУППУ. Добавление в нашу систему возможно только для Мероприятий(Встреч) из ВК.')
                    elif resp['response'][0]['type'] == "page":
                            messages.add_message(request, messages.INFO, 'Вы пытаетесь добавить ПАБЛИК. Добавление в нашу систему возможно только для Мероприятий(Встреч) из ВК.')
                    else:
                        messages.add_message(request, messages.INFO, 'Вы пытаетесь добавить %s. Добавление в нашу систему возможно только для Мероприятий(Встреч) из ВК.' % resp['response'][0]['type'])

                    try:
                        if (resp['response'][0]['city'],) not in LocationCities.objects.values_list('vk_city_id'):
                            messages.add_message(request, messages.ERROR, 'К сожалению, мы пока не работаем в городе, указаном в Местоположении вашего мероприятия.')
                    except (KeyError, IndexError):
                        messages.add_message(request, messages.ERROR, 'В вашем мероприятии не заполнено поле "Местоположение".')

                except (KeyError, IndexError):
                    logger.error('Ошибка запроса %s с данными %s' % (url, event_screen_name))
            else:
                messages.add_message(request, messages.ERROR, 'Не удалось получить данные по указанной вами ссылке. Пожалуйста, убедитесь в корректности введённх вами данных и повторите попытку.')

            if 'error' in resp:
                if resp['error']['error_code'] == 100:
                    messages.add_message(request, messages.ERROR, 'Указанная вами ссылка не существует.')

            if messages.get_messages(request):
                return redirect('add_failed')

            sys.path.append('/home/dell/scripts/py_class/')
            from c_vk_events import VkEvents
            parse_result = VkEvents().parse_vk_groups([event_id], safely=True, site=True)
            if parse_result:
                messages.add_message(request, messages.SUCCESS, parse_result[0]['name'])

                if not request.user.is_staff:
                    mail_title = 'Новый запрос на добавление мероприятия из VK'
                    mail_body = 'Мероприятие "%s" ожидает модерации. \n\n%s' % (parse_result[0]['name'],
                                                                                parse_result[0]['description'])
                    modaration_url = "http://mod.vkalendare.com/?search=%d" % event_id
                    mail_body = mail_body + '\n' + modaration_url

                    mail_result = send_mail(
                        mail_title,
                        mail_body,
                        'admin@vkalendare.com',
                        ['dell.oxl@gmail.com', 'pr@vkalendare.com'],
                        fail_silently=False,
                    )
                return redirect('add_successfully')
        else:
            return redirect('add_event_form')
    return render(request, 'add_event_selector.html')


def add_event_form(request):
    if request.user.is_anonymous():
        request.session['add_event_form_http_referer'] = 1
        return redirect('login', )
    context = {}
    context['form'] = AddNewEvent(request.POST, request.FILES)
    context['locations'] = Locations.objects.exclude(created=0, is_deleted=1).order_by('name').all()
    # new_place_data = {'logo': 'http://', 'url': ''}
    context['org_form'] = CustomPlacesForm(prefix='new_org')
    # context['org_form']['name'].css_classes('foo bar')
    context.update(csrf(request))
    if request.POST:
        # Delete every non utf-8 symbols froms string
        request.POST['title'] = request.POST['title'].encode("utf-8").decode('utf-8', 'ignore')
        request.POST['description'] = request.POST['description'].encode("utf-8").decode('utf-8', 'ignore')

        new_org_flag = False
        if 'new_org-name' in request.POST.keys():
            CustomPlacesFormObj = CustomPlacesForm(request.POST, prefix='new_org')
            if CustomPlacesFormObj.is_valid():
                org_obj = CustomPlacesFormObj.save(commit=False)
                new_org_flag = True
                request.POST['place_id'] = org_obj.id

        p = pill(request.FILES['image'])
        img_file = InMemoryUploadedFile(p[0], None, 'poster.jpg', 'image/jpeg', p[0].tell, None)
        thumb_file = InMemoryUploadedFile(p[1], None, 'thumb.jpg', 'image/jpeg', p[1].tell, None)
        request.FILES['image'] = img_file
        request.FILES['thumb'] = thumb_file
        if request.user.is_staff:
            request.POST['export_vk'] = 1
            request.POST['is_active'] = 1
        else:
            request.POST['export_vk'] = 9
            request.POST['is_active'] = 9
        new_event_form = AddNewEvent(request.POST, request.FILES)
        if new_event_form.is_valid():
            location = Locations.objects.get(pk=request.POST['location'])
            if new_org_flag:
                org_obj.location = location
                if request.user.is_staff:
                    org_obj.status = 2
                else:
                    org_obj.status = 0
                org_obj.save()
                new_event_form.place = org_obj
            else:
                new_event_form.place = request.POST['place']

            new_event_form.title = request.POST['title']
            new_event_form.description = request.POST['description']
            new_event_form.location = request.POST['location']
            new_event_form.start_time = request.POST['start_time']
            new_event_form.start_date = request.POST['start_date']

            new_event_form.image = request.FILES['image']
            new_event_form.thumb = request.FILES['thumb']
            if 'is_free' in request.POST:
                new_event_form.is_free = 1
            else:
                new_event_form.is_free = 0
            # res = new_event.save()
            context['form'] = new_event_form
            if new_event_form.is_valid():
                obj = new_event_form.save(commit=False)
                obj.owner = request.user
                obj.save()
                obj.url = 'http://vkalendare.com/%s/%s' % (location.site_screen_name,
                                                           obj.id)
                obj.save()
                new_event_form.save_m2m()
                response = {'status': 'OK',
                            'Cache-Control': 'no-cache',
                            'redirect': request.build_absolute_uri(reverse('added_successfully'))}

                if not request.user.is_staff:
                    mail_title = 'Новый запрос на добавление мероприятия'
                    mail_body = 'Мероприятие "%s" ожидает модерации. \n\n%s' % (request.POST['title'],
                                                                                request.POST['description'])
                    modaration_url = "http://vkalendare.com/admin/mysite/events/?export_vk__exact=9"
                    if new_org_flag:
                        mail_title = 'Запрос на добавление мероприятия с НОВЫМ МЕСТОМ!'
                        place_body = 'Запрос на добавление нового места: "%s" в городе %s. \n' % (org_obj.name,
                                                                                                  obj.location.name)
                        mail_body = place_body + mail_body

                    mail_body = mail_body + '\n' + modaration_url

                    mail_result = send_mail(
                        mail_title,
                        mail_body,
                        'admin@vkalendare.com',
                        ['dell.oxl@gmail.com', 'pr@vkalendare.com'],
                        fail_silently=False,
                    )
                    response['notification'] = mail_result
                return HttpResponse(json.dumps(response), content_type='application/json')
                # return HttpResponseRedirect(request.build_absolute_uri(reverse('added_successfully')))
                # return redirect(added_successfully)
                # response = {'status': 0,
                #             'site_screen_name': obj.location.site_screen_name,
                #             'pk': obj.pk,
                #             'title_translit': 'new',
                #             'url': 'event_details'}
                # return HttpResponse(json.dumps({'error_code': 0}), content_type='application/json')
                # return HttpResponse(json.dumps(response), content_type='application/json')
                # return redirect('added_successfully')
            else:
                return HttpResponseBadRequest
        else:
            response = {'status': 'error', 'message': new_event_form.errors}
            return HttpResponse(json.dumps(response), content_type='application/json')
                # return redirect('event_details', site_screen_name=obj.location.site_screen_name, pk=obj.pk, title_translit='new')
    return render(request, 'add_event_form.html', context)


def add_successfully(request):
    return render(request, 'mysite/templates/mysite/add_successfully.html')


def add_failed(request):
    return render(request, 'mysite/templates/mysite/add_failed.html')


def admin_list(request):
    if request.method == "POST":
        if request.POST['task'] == 'set_active':
            event = Events.objects.get(pk=request.POST['event_id'])
            event.is_active = 1
            event.export_vk = 1
            event.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

        if request.POST['task'] == 'set_active_with_priority':
            event = Events.objects.get(pk=request.POST['event_id'])
            event.is_active = 1
            event.export_vk = 1
            event.priority = 1
            event.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

        if request.POST['task'] == 'set_dismiss':
            event = Events.objects.get(pk=request.POST['event_id'])
            event.is_active = 0
            event.export_vk = 0
            event.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')


def jdata(request):
    if request.method == "POST":
        if request.POST['task'] == 'get_location_places':
            # sql_query = "SELECT * from mysite_organizers where id in (SELECT DISTINCT organizer_id from mysite_events WHERE location_id = %s) AND confidence > 1 AND vk_type = 'group' ORDER BY followers" % request.POST['location_id']
            #
            # places = MysiteOrganizers.objects.raw(sql_query)
            places = Customplaces.objects.filter(location=request.POST['location_id']).exclude(is_deleted=1).order_by(
                '-org_parent__followers')
            # places = Events.local_organizer
            # places = Events.objects.get(pk=request.POST['location_id'])
            d = []
            for place in places:
                d.append({'id': place.id,
                          'name': place.name,
                          'logo': place.logo,
                          'url': place.url})
            return HttpResponse(json.dumps({'location_places': d}), content_type='application/json')


def add_tags_for_event(event_obj):
    logger.info(event_obj)
    morph = pymorphy2.MorphAnalyzer()
    tags = []
    for w in re.sub('[^а-яА-Я]', ' ', event_obj.title).strip().split(' '):
        if len(w) > 2:
            p = morph.parse(w)[0]
            if 'NOUN' in p.tag:
                tags.append(p.normal_form)

    from nltk import PorterStemmer
    from nltk import pos_tag
    stemmer = PorterStemmer()
    text = nltk.word_tokenize(re.sub('[^a-zA-Z]', ' ', event_obj.title))
    [tags.append(stemmer.stem(w).lower()) for (w, b) in pos_tag(text) if b.startswith('NN') or b.startswith('JJ')]

    for tag in tags:
        event_obj.tag_it.add(tag)

    logger.info(tags)
    return ','.join(tags)


@csrf_exempt
def set_tags(request):
    future_days = 90
    if request.GET['task'].isdigit():
        events_for_taggit = Events.objects.filter(pk=request.GET['task'])
    elif request.GET['task'] == 'all_future':
        events_for_taggit = Events.objects.exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=future_days))
    elif request.GET['task'] == 'empty':
        events_for_taggit = Events.objects.filter(tag_it__isnull=True)[:100]
    elif request.GET['task'] == 'empty_future':
        events_for_taggit = Events.objects.exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=future_days)).filter(tag_it__isnull=True)
        # return HttpResponse(json.dumps({'tags': False}), content_type='application/json')

    tags = ''
    for event in events_for_taggit:
        tags = add_tags_for_event(event)
    # Events.tag_it.most_common().values_list()
    # Events.objects.filter(tag_it__name__in=["рок"])
    return HttpResponse(json.dumps({'tags': tags}), content_type='application/json')


def jservice(request):
    if request.GET['task'] == 'set_custom_places':
        events_for_taggit = Events.objects.exclude(start_date__lte=today).exclude(
            start_date__gte=today + timedelta(days=90))
        return HttpResponse(json.dumps({'result': True}), content_type='application/json')

    if request.GET['task'] == 'orgs_to_places':
        location_id = 6
        sql_query = "SELECT * from mysite_organizers where id in (SELECT DISTINCT organizer_id from mysite_events WHERE location_id = %s) AND confidence = 2 AND vk_type = 'group' ORDER BY followers" % location_id
        places = MysiteOrganizers.objects.raw(sql_query)

        # data['location'] = location_id

        for place in places:
            if not Customplaces.objects.filter(org_parent=place.id).count():
                data = {'name': place.name,
                        'logo': place.logo,
                        'url': place.url}
                CustomPlacesFormObj = CustomPlacesForm(data)
                if CustomPlacesFormObj.is_valid():
                    obj = CustomPlacesFormObj.save(commit=False)
                    obj.org_parent = MysiteOrganizers.objects.get(pk=place.id)
                    obj.location = Locations.objects.get(pk=location_id)
                    obj.status = place.confidence
                    obj.save()
                    pass
        return HttpResponse(json.dumps({'result': True}), content_type='application/json')

    if request.GET['task'] == 'push_confidence':
        push_confidence()
        return HttpResponse(json.dumps({'result': True}), content_type='application/json')

    if request.GET['task'] == 'update_event':
        update_event([134224605])
        return HttpResponse(json.dumps({'result': True}), content_type='application/json')

    if request.GET['task'] == 'test':
        mail_title = 'Новый запрос на добавление мероприятия'
        mail_body = 'Мероприятие "%s" ожидает модерации. \n\n%s' % ('ЗАГОЛОВОК',
                                                                    'ОПИСАНИЕ')
        modaration_url = "http://vkalendare.com/admin/mysite/events/?export_vk__exact=9"
        if True:
            mail_title = 'Запрос на добавление мероприятия с НОВЫМ МЕСТОМ!'
            place_body = 'Запрос на добавление нового места: "%s" в городе %s. \n' % ("MESTO",
                                                                                      "CITY")
            mail_body = place_body + mail_body
        mail_body = mail_body + '\n' + modaration_url
        mail_result = send_mail(
            mail_title,
            mail_body,
            'admin@vkalendare.com',
            ['dell.oxl@gmail.com', 'pr@vkalendare.com'],
            fail_silently=False,
        )
        return HttpResponse(json.dumps({'result': True}), content_type='application/json')


def update_event(vk_events_list):
    # vk_events_list = [49611313]
    result = {'events': []}
    vk_events_for_update = MysiteVkEvents.objects.filter(id__in=vk_events_list)
    for vk_event in vk_events_for_update:
        event = Events.objects.get(pk=vk_event.event_id)
        r = requests.get(vk_event.image_url, stream=True)
        if not r.status_code == requests.codes.ok:  # попробуем в следующий раз
            logger.error('Не удалось скачать афишу для мероприятия: %s' % event.url)
            continue
        r.raw.decode_content = True
        p = pill(r.raw)
        event.image = InMemoryUploadedFile(p[0], None, 'poster.jpg', 'image/jpeg', p[0].tell, None)
        event.thumb = InMemoryUploadedFile(p[1], None, 'thumb.jpg', 'image/jpeg', p[1].tell, None)
        logger.debug(event.image)
        event.save()
        result['events'].append(event.title)
    result['status'] = 'Success'
    return result


def push_confidence(priority=0, local_tz=10800, event_id=None):
    result = {'status': 'Success'}
    events_for_approve = MysiteVkEvents.objects.filter(
        created__lt=int((datetime.utcnow() - timedelta(days=1)).timestamp()),
        start__lt=int((datetime.utcnow() + timedelta(days=14)).timestamp()),
        members__gt=0, image_url__isnull=False, is_new=1, event_id__isnull=True,
        organizer_id__confidence=2)
    for vk_event in events_for_approve:
        logger.info(vk_event)
        event_location = LocationCities.objects.get(vk_city_id=vk_event.city_id)
        tz = event_location.location.tz
        if tz:
            if abs(tz) < 3600:
                tz *= 3600

            dtime = datetime.utcfromtimestamp(vk_event.start + tz)
        else:
            # dtime = datetime.fromtimestamp(vk_event.start, tz=tzlocal.get_localzone())
            # dtime = dtime.replace(tzinfo=None)

            # dtime = datetime.fromtimestamp(vk_event.start).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone())

            # local_tz = tzlocal.get_localzone().utcoffset(datetime.utcfromtimestamp(vk_event.start)).seconds
            dtime = datetime.utcfromtimestamp(vk_event.start + local_tz)

        event_date = {}
        event_date['title'] = vk_event.name
        event_date['description'] = vk_event.description
        event_date['location'] = event_location.location_id
        event_date['start_date'] = dtime.date()
        event_date['start_time'] = dtime.time()
        event_date['url'] = 'http://vk.com/event%d' % vk_event.id
        event_date['organizer'] = vk_event.organizer_id
        event_date['priority'] = priority
        event_date['is_active'] = 1
        event_date['export_vk'] = 1
        if vk_event.finish:
            if 60 < (vk_event.finish - vk_event.start) < 604800:
                if tz:
                    finish_dtime = datetime.utcfromtimestamp(vk_event.finish + tz)
                else:
                    # finish_dtime = datetime.fromtimestamp(vk_event.finish, tz=tzlocal.get_localzone())
                    local_tz_finish = tzlocal.get_localzone().utcoffset(
                        datetime.utcfromtimestamp(vk_event.finish)).seconds
                    finish_dtime = datetime.utcfromtimestamp(vk_event.finish + local_tz_finish)

                event_date['finish_date'] = finish_dtime.date()
                event_date['duration'] = vk_event.finish - vk_event.start
        logger.debug('vk_event.start: %s, tx: %s' % (vk_event.start, tz))

        ConfidenceNewEventObj = ConfidenceNewEvent(event_date)
        if ConfidenceNewEventObj.is_valid():
            r = requests.get(vk_event.image_url, stream=True)
            if not r.status_code == requests.codes.ok:  # попробуем в следующий раз
                logger.error('Не удалось скачать афишу для мероприятия: %s' % event_date['url'])
                continue
            r.raw.decode_content = True
            p = pill(r.raw)
            img_file = InMemoryUploadedFile(p[0], None, 'poster.jpg', 'image/jpeg', p[0].tell, None)
            thumb_file = InMemoryUploadedFile(p[1], None, 'thumb.jpg', 'image/jpeg', p[1].tell, None)
            FILES = {'image': img_file, 'thumb': thumb_file}
            ConfidenceNewEventObj = ConfidenceNewEvent(event_date, FILES)
            ConfidenceNewEventObj.image = img_file
            ConfidenceNewEventObj.thumb = thumb_file

            if ConfidenceNewEventObj.is_valid():
                obj = ConfidenceNewEventObj.save()
                vk_event.is_new = 0
                vk_event.event_id = obj.id
                vk_event.save()
                logger.info('Добавлено: %s' % event_date['title'])
    result['events_for_approve'] = events_for_approve

    events_for_reject = MysiteVkEvents.objects.filter(is_new=1, event_id__isnull=True, organizer_id__confidence=3)
    for vk_reject_event in events_for_reject:
        vk_reject_event.is_new = 0
        vk_reject_event.save()
        logger.info('Отклонено: %s' % vk_reject_event.name)
    result['events_for_reject'] = events_for_reject

    result['status'] = 'Success'
    return result


# ->leftJoin('Organizers', 'VkEvents.organizer_id=Organizers.id')
# ->groupBy('VkEvents.id')
# ->where('VkEvents.members > 0')
#
# ->andWhere('VkEvents.image_url IS NOT NULL')
# ->andWhere('VkEvents.is_new=1')
# ->andWhere('VkEvents.event_id IS NULL')
# ->andWhere('VkEvents.created < UNIX_TIMESTAMP()-86400')
# ->andWhere('VkEvents.start < UNIX_TIMESTAMP()+1209600')
# ->andWhere('Organizers.confidence=2');


@staff_member_required
def my_admin_view(request):
    return render_to_response(r'admin/mysite/events/admin_service.html')


@csrf_exempt
def set_user_location(request):
    if 'id' in request.POST:
        request.session['user_location'] = request.POST['id']
        request.session.modified = True
        user_location = Locations.objects.get(id=request.POST['id'])
        if request.user.is_authenticated:
            usr = request.user
            usr.location = user_location
            usr.save()
        request.user.location = user_location
        return HttpResponse(json.dumps({'status': True, 'city': user_location.name}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'status': False}), content_type='application/json')


def create_organizer(request):
    if request.user.is_anonymous():
        request.session['add_event_form_http_referer'] = 1
        return redirect('login', )
    context = {}
    context['form'] = CustomPlacesForm(request.POST, request.FILES)
    context.update(csrf(request))
    if request.POST:
        new_event_form = CustomPlacesForm(request.POST)
        if new_event_form.is_valid():
            new_event_form.vk_id = request.POST['vk_id']
            new_event_form.vk_type = request.POST['vk_type']
            new_event_form.name = request.POST['name']
            new_event_form.logo = request.POST['logo']
            new_event_form.url = request.POST['url']
            new_event_form.followers = request.POST['followers']
            new_event_form.place_id = request.POST['place_id']

            # context['form'] = new_event_form
            if new_event_form.is_valid():
                obj = new_event_form.save(commit=False)
                obj.owner = request.user
                obj.save()
                new_event_form.save_m2m()
                response = {'redirect': request.build_absolute_uri(reverse('added_successfully'))}
                return HttpResponse(json.dumps(response), content_type='application/json')

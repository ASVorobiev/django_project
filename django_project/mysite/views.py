import copy
import hashlib
import json
import os
from datetime import date, timedelta
from io import BytesIO
from io import StringIO
from time import sleep


from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from httplib2 import Response

from django_project.mysite.forms import AddNewEvent
from django_project.mysite.models import Events, Locations
from transliterate import translit

today = date.today()


# Create your views here.


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
    return render(request, 'mysite/event_details.html', {'event_data': event_data,
                                                         'current_location': current_location,
                                                         'locations': locations,
                                                         'title_translit': translit(event_data.title, 'ru',
                                                                                    reversed=True).replace(' ', '_')
                                                         })
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps


def pill(image_io):
    im = Image.open(image_io)
    # im = Image.open(StringIO.StringIO(buffer))


    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.load_default()
    # draw.text((x, y),"Sample Text",(r,g,b))
    # draw.text((0, 0),"Sample Text",(255,255,255),font=font)
    # draw.line((0, 10, 200, 200), fill=100, width=100)

    (width, height) = im.size
    p_height = int(height * 0.05)
    ltrb_border = (0, 0, 0, p_height)
    im_with_border = ImageOps.expand(im, border=ltrb_border, fill='white')

    draw = ImageDraw.Draw(im_with_border)
    # draw.text((10, height), "Информационная поддержка: Проект 'Афиша вКалендаре'", fill='black', font=font)
    draw.text((10, height), "Support: vKalendare.com", fill='black', font=font)
    # im_with_border.show()



    buffer = BytesIO()
    # thumb.save(buffer, "PNG")
    im_with_border.save(fp=buffer, format='JPEG')
    s = buffer.getvalue()
    im_file = ContentFile(s)



    size = 128, 128
    # outfile = os.path.splitext(file_address)[0] + "_thumbnail.jpg"
    im.thumbnail(size, Image.ANTIALIAS)
    buffer2 = BytesIO()
    im.save(buffer2, "JPEG")
    s2 = buffer2.getvalue()
    thumb_file = ContentFile(s2)
    return im_file, thumb_file


def image_save(image):
    md = hashlib.md5(image.file.getvalue()).hexdigest()
    print(md)
    n = 2
    local_path = ''
    for dr in [md[i:i+n] for i in range(0, len(md), n)]:
        local_path = os.path.join(local_path, dr)

    file_address = os.path.join(local_path, 'poster.jpg')
    # tmp = 'C:\\tmp\\'
    abs_file_path = os.path.join(settings.MEDIA_ROOT, file_address)
    # file_address = os.path.join(tmp, file_address)
    os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    import copy
    im_copy = copy.deepcopy(image)
    pth = pill(im_copy)
    return os.path.join(local_path, pth[0]), os.path.join(local_path, pth[1])
    # return '3f\\98\\ff\\1a\\aa\\37\\62\\c6\\89\\1e\\54\\e0\\d2\\68\\5f\\df\\poster.jpg', '3f\\98\\ff\\1a\\aa\\37\\62\\c6\\89\\1e\\54\\e0\\d2\\68\\5f\\df\\poster.jpg'


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
        pth = pill(request.FILES['image'])
        # new_event.image = '3f\\98\\ff\\1a\\aa\\37\\62\\c6\\89\\1e\\54\\e0\\d2\\68\\5f\\df\\poster.jpg'
        # new_event.thumb = '3f\\98\\ff\\1a\\aa\\37\\62\\c6\\89\\1e\\54\\e0\\d2\\68\\5f\\df\\poster.jpg'
        # im_copy = copy.deepcopy(request.FILES['image'])
        # pth = pill(im_copy)

        # model_instance.image_field.save(model_instance.image_field.name,
        #                                 ContentFile(f.getvalue()))
        # new_event.image = ('im', ContentFile(pth[0]))
        # new_event.image = pth[0]

        # new_event.thumb = pth[1]
        thumb_file = InMemoryUploadedFile(pth[0], None, 'foo.jpg', 'image/jpeg',
                                          pth[0].tell, None)

        new_event.start_time = request.POST['start_time']
        new_event.start_date = request.POST['start_date']
        # old = request.FILES['image']
        request.FILES['image'] = thumb_file
        new_event.image = request.FILES['image']
        new_event.thumb = request.FILES['image']
        # new_event.image = thumb_file
        # print('image', new_event.image)
        # print('thumb', new_event.thumb)
        res = new_event.save()
        print(res)
        # event.location.site_screen_name
        # event.id
        # event.title_translit | urlencode
        return redirect('event_details', site_screen_name=res.location.site_screen_name, pk=res.pk, title_translit='new')
    return render(request, 'mysite/add_event_form.html', context)


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
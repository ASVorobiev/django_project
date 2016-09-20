import json
from time import sleep
import json

import requests as requests
from django.conf import settings
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseBadRequest, request
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from social.apps.django_app.utils import psa
from social.backends.google import GooglePlusAuth
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.utils import load_backends

from django_project.text_ru.forms import TextForm


def base(request):
    return render(request, 'text_ru.html', {})


def send_text_form(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        context['text'] = TextForm(request.POST)
        context['message'] = request.POST['input_name']
        # context['text_ru'] = send_text(context['message'])
        return render(request, 'text_ru.html', context)
    return render(request, 'text_ru.html', context)


def send_text(text):
    post_url = 'http://api.text.ru/post'
    userkey = '1d85c68d1c2bfb861b965c7754de9ce8'
    post_data = {
        'text': text,
        'userkey': userkey}
    send_response = requests.post(post_url, data=post_data).json()
    print(send_response)

    if 'error_code' not in send_response:
        post_req = {'userkey': userkey,
                    'uid': send_response['text_uid'],
                    'jsonvisible': 'detail'}
        get_response = requests.post(post_url, data=post_req).json()
        while 'error_code' in get_response:
            print(get_response)
            sleep(1)
            get_response = requests.post(post_url, data=post_req).json()
            # get_response = {'spell_check': '[{"error_type":"\\u041f\\u0440\\u043e\\u0432\\u0435\\u0440\\u043a\\u0430 \\u043e\\u0440\\u0444\\u043e\\u0433\\u0440\\u0430\\u0444\\u0438\\u0438","replacements":["\\u043a\\u043e\\u043f\\u0438\\u0440\\u0430\\u0439\\u0442 \\u0438\\u043d\\u0433\\u0430"],"reason":"\\u041d\\u0430\\u0439\\u0434\\u0435\\u043d\\u0430 \\u043e\\u0440\\u0444\\u043e\\u0433\\u0440\\u0430\\u0444\\u0438\\u0447\\u0435\\u0441\\u043a\\u0430\\u044f \\u043e\\u0448\\u0438\\u0431\\u043a\\u0430","error_text":"\\u043a\\u043e\\u043f\\u0438\\u0440\\u0430\\u0439\\u0442\\u0438\\u043d\\u0433\\u0430","start":84,"end":95}]', 'unique': '0.00', 'result_json': '{"date_check":"19.09.2016 19:32:38","unique":0,"clear_text":"\\u0421\\u0443\\u0449\\u0435\\u0441\\u0442\\u0432\\u0443\\u0435\\u0442 \\u0433\\u043b\\u0443\\u0431\\u043e\\u043a\\u0438\\u0439 \\u0440\\u0435\\u0440\\u0430\\u0439\\u0442\\u0438\\u043d\\u0433 \\u0438\\u043b\\u0438 \\u043f\\u0435\\u0440\\u0435\\u0441\\u043a\\u0430\\u0437 \\u0447\\u0443\\u0436\\u0438\\u0445 \\u0442\\u0435\\u043a\\u0441\\u0442\\u043e\\u0432 \\u0441 \\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435\\u043c \\u044d\\u043b\\u0435\\u043c\\u0435\\u043d\\u0442\\u043e\\u0432 \\u043a\\u043e\\u043f\\u0438\\u0440\\u0430\\u0439\\u0442\\u0438\\u043d\\u0433\\u0430 \\u043a\\u043e\\u0433\\u0434\\u0430 \\u0440\\u0430\\u0437\\u0440\\u0435\\u0448\\u0430\\u0435\\u0442\\u0441\\u044f \\u0438\\u0437\\u043c\\u0435\\u043d\\u044f\\u0442\\u044c \\u0441\\u0442\\u0438\\u043b\\u044c \\u043a\\u043e\\u043d\\u0442\\u0435\\u043d\\u0442\\u0430 \\u0434\\u043e\\u0431\\u0430\\u0432\\u043b\\u044f\\u0442\\u044c \\u0438\\u043d\\u0444\\u043e\\u0440\\u043c\\u0430\\u0446\\u0438\\u044e \\u0438 \\u043f\\u0440 \\u0420\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u0430\\u043d\\u044b \\u0441\\u043f\\u0435\\u0446\\u0438\\u0430\\u043b\\u044c\\u043d\\u044b\\u0435 \\u043a\\u043e\\u043c\\u043f\\u044c\\u044e\\u0442\\u0435\\u0440\\u043d\\u044b\\u0435 \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u044b \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0435 \\u043f\\u043e\\u0437\\u0432\\u043e\\u043b\\u044f\\u044e\\u0442 \\u0440\\u0430\\u0437\\u043c\\u043d\\u043e\\u0436\\u0430\\u0442\\u044c \\u0442\\u0435\\u043a\\u0441\\u0442\\u044b \\u0437\\u0430\\u043c\\u0435\\u043d\\u044f\\u044f \\u043e\\u0442\\u0434\\u0435\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0438\\u0441\\u0445\\u043e\\u0434\\u043d\\u044b\\u0435 \\u0441\\u043b\\u043e\\u0432\\u0430 \\u0441\\u0438\\u043d\\u043e\\u043d\\u0438\\u043c\\u0430\\u043c\\u0438","mixed_words":"","urls":[{"url":"http:\\/\\/vk.com\\/wall-91072377","plagiat":100,"words":"0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32"},{"url":"http:\\/\\/pr-cy.ru\\/lib\\/seo\\/Kontent-sayta-SEO-kopirayting-Unikal-nost-kontenta","plagiat":100,"words":"0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32"}]}', 'seo_check': '{"count_chars_with_space":297,"count_chars_without_space":265,"count_words":33,"water_percent":6,"list_keys":[{"count":2,"key_title":"\\u0442\\u0435\\u043a\\u0441\\u0442\\u043e\\u0432"}],"list_keys_group":[{"count":2,"key_title":"\\u0442\\u0435\\u043a\\u0441\\u0442\\u043e\\u0432","sub_keys":[]}],"spam_percent":29,"mixed_words":[]}', 'text_unique': '0.00'}
        spell_check = json.loads(get_response['spell_check'])
        seo_check = json.loads(get_response['seo_check'])
        result_json = json.loads(get_response['result_json'])
        # print(spell_check)
        # print(seo_check)
        # print('RESULT: ', get_response)
    else:
        print('ERROR')
        print(send_response)

    # return get_response
    return {'result_json': result_json,
            'seo_check': seo_check,
            'spell_check': spell_check,
            'text_unique': get_response['text_unique'],
            'unique': get_response['unique'],
            'text_uid': send_response['text_uid']
            }


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         # user = authenticate(username=username, password=password)
#         if 'qwe' is not None:
#             # login(request, user)
#             return HttpResponse({'message': request.POST.get('input_name'),
#                                  'unique': 100},
#                                 content_type='text/html')
#         else:
#             return HttpResponse('неверный логин/пароль!', content_type='text/html')
#     else:
#         return HttpResponse('Ошибка авторизации!', content_type='text/html')


def advert(request):
    # context = {}
    #context.update(csrf(request))
    if request.method == "POST":
        form = TextForm(request.POST)
        # if form.is_valid():
        context = {'unique': '0.00', 'seo_check': {'count_chars_with_space': 110, 'mixed_words': [], 'spam_percent': 22, 'list_keys': [{'count': 2, 'key_title': 'друг'}], 'count_words': 15, 'count_chars_without_space': 96, 'water_percent': 16, 'list_keys_group': [{'count': 2, 'sub_keys': [], 'key_title': 'друг'}]}, 'text_unique': '0.00', 'spell_check': [], 'result_json': {'clear_text': 'На основе одного шаблона генерируется множество статей с невысокой уникальностью очень похожих друг на друга', 'urls': [{'url': 'http://vk.com/wall-91072377', 'plagiat': 100, 'words': '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14'}, {'url': 'http://pr-cy.ru/lib/seo/Kontent-sayta-SEO-kopirayting-Unikal-nost-kontenta', 'plagiat': 100, 'words': '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14'}], 'unique': 0, 'mixed_words': '', 'date_check': '19.09.2016 19:58:30'}, 'text_uid': '57e0192d87fb8'}

        #context['text_ru'] = send_text(request.POST['description'])
        # context['text_ru'] =
        urls = []
        for url in context['result_json']['urls']:
            if url['plagiat'] > 70:
                urls.append({'url': url['url']})
            else:
                print('Уникальность описания больше 30%')
        context['urls'] = urls

        sleep(0.1)
        return HttpResponse(json.dumps(context), content_type='application/json')

    # return render_to_response('text_ru.html',
    #         {'form': TextForm()}, RequestContext(request))
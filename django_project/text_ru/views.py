import json
from time import sleep
import json

import requests as requests
from django.conf import settings
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseBadRequest, request
from django.shortcuts import redirect, render
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
        context['text_ru'] = send_text(context['message'])
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
        spell_check = json.loads(get_response['spell_check'])
        seo_check = json.loads(get_response['seo_check'])
        print(spell_check)
        print(seo_check)
        print('RESULT: ', get_response)
    else:
        print('ERROR')
        print(send_response)

    return {'text_ru': get_response,
            'text_uid': send_response['text_uid'],
            'unique': get_response['unique']
            }

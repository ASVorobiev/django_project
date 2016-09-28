import json

from django.conf import settings
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from social.apps.django_app.utils import psa
from social.backends.google import GooglePlusAuth
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.utils import load_backends

from django_project.user_auth.decorators import render_to


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)


@render_to('auth.html')
def home(request):
    """Home view, displays login mechanism"""
    request.session['http_referer_foo'] = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated():
        return redirect(request.META.get('HTTP_REFERER'))
    return context()


@login_required
@render_to('auth.html')
def done(request):
    """Login complete view, displays user data"""
    try:
        if request.session._session['add_event_form_http_referer']:
            request.session._session['add_event_form_http_referer'] = False
            return redirect('/add_event_form')
    except KeyError:
        print('add_event_form_http_referer no found')
    try:
        return redirect(request.session._session['http_referer_foo'])
    except TypeError:
        return redirect(request.META.get('HTTP_REFERER'))



@render_to('auth.html')
def validation_sent(request):
    return context(
        validation_sent=True,
        email=request.session.get('email_validation_address')
    )


@render_to('auth.html')
def require_email(request):
    backend = request.session['partial_pipeline']['backend']
    return context(email_required=True, backend=backend)


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')

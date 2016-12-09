#-*- coding: utf-8 -*-

import sys
from sys import platform as _platform
from os.path import abspath, dirname, join
import os


sys.path.insert(0, '../..')

DEBUG = True

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
    ('dell', 'dell.oxl@gmail.com'),
)


MANAGERS = ADMINS
# noinspection PyPackageRequirements
ALLOWED_HOSTS = ['0.0.0.0', 'vkalendare.net', '.vkalendare.com', '127.0.0.1', '192.168.0.1/24', '[::1]']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vkalendare_site',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
if _platform == "linux" or _platform == "linux2":
    pass
elif _platform == "win32":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'local_server',
            'USER': 'root',
            'PASSWORD': 'Qwerty123',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        }
    }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'vkalendare',
#         'USER': 'postgres',
#         'PASSWORD': 'Qwerty123',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False
# MEDIA_ROOT = 'C:\\vKalendare\\storage'
MEDIA_ROOT = '/home/www/vkalendare.net/mod/storage'
MEDIA_URL = '/storage/'
DATE_FORMAT = 'd E Y'

STATIC_ROOT = os.path.join(ROOT_PATH, 'django_project', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, 'django_project/mysite/static'),
    os.path.join(ROOT_PATH, 'django_project/about/static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '#$5btppqih8=%ae^#&amp;7en#kyi!vh%he9rg=ed#hm6fnw9^=umc'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'django_project.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [join(ROOT_PATH, 'templates'),
                 os.path.join(ROOT_PATH, 'django_project', 'mysite', 'templates', 'mysite'),
                 os.path.join(ROOT_PATH, 'django_project', 'about', 'templates'),
                 os.path.join(ROOT_PATH, 'django_project', 'mysite', 'templates', 'admin', 'mysite', 'events'),
                 os.path.join(ROOT_PATH, 'django_project', 'mysite', 'templates', 'el_pagination'),
                 os.path.join(ROOT_PATH, 'django_project', 'mysite', 'templatetags'),
                 os.path.join(ROOT_PATH, 'django_project', 'user_auth', 'templates'),
                 os.path.join(ROOT_PATH, 'django_project', 'text_ru', 'templates'),
                 os.path.join(ROOT_PATH, 'django_project'),
                 r'C:\vKalendare\Github\django_project\django_project\mysite\templates\mysite'
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': ['django.contrib.auth.context_processors.auth',
                                   # 'django.core.context_processors.debug',
                                   # 'django.core.context_processors.i18n',
                                   # 'django.core.context_processors.media',
                                   'django.template.context_processors.request',
                                   'django.contrib.messages.context_processors.messages',
                                   'social.apps.django_app.context_processors.backends'],
            #'loaders': [#'django.template.loaders.filesystem.Loader',
                        #'django.template.loaders.app_directories.Loader',
                        #     'django.template.loaders.eggs.Loader',
            #            ],
            'debug': DEBUG,
            # ... some options here ...
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'django_project.user_auth',
    'django_project.mysite',
    'django_project.text_ru',
    'el_pagination',
    'taggit',
    'django_project.mysite.templatetags.myfilters',
    'django_project.mysite.templatetags.shuffle',
    'django_project.about',
    # 'xadmin',
    # 'crispy_forms',
    # 'reversion',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/usr/home/www/vkalendare.com/logs/django_main.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/usr/home/www/vkalendare.com/logs/django_main_debug.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'null': {
            "class": 'logging.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}

if _platform == "win32":
    LOGGING['handlers']['production_file']['filename'] = '../logs/django_main.log'
    LOGGING['handlers']['debug_file']['filename'] = '../logs/django_main_debug.log'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.instagram.InstagramOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.vk.VKOAuth2',
    'social.backends.yandex.YandexOAuth2',
    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'user_auth.CustomUser'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/done/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/user_auth/drive',
    'https://www.googleapis.com/user_auth/userinfo.profile'
]
# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
# SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'django_project.user_auth.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

EMAIL_FROM = ''
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'django_project.user_auth.pipeline.require_email',
    # 'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['first_name', 'last_name', 'email',
#                                         'username']
#
# try:
#     from example.local_settings import *
# except ImportError:
#     pass

# https://vk.com/editapp?id=5618522&section=options
SOCIAL_AUTH_VK_OAUTH2_KEY = '5618522'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'QaEBvN2GbCRdHdSr1PhU'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'groups']

# https://console.developers.google.com/apis/credentials?project=vkalendare-142519
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '413629303380-bmkjgoesma17348chttgv3uf8p1k12o9.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '_DFPu4WdsMZZnfZKhz84rxM7'

# https://ok.ru/game/1248113664
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = '1248113664'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = '6FE117552FC5F8F4315113C4'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = 'CBAFLFGLEBABABABA'

# https://developers.facebook.com/apps/1656433434670180/settings/basic/
SOCIAL_AUTH_FACEBOOK_KEY = '1656433434670180'
SOCIAL_AUTH_FACEBOOK_SECRET = '48af44efd8a8fa7906ccf84fdf456d5c'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'ru_RU',
    'fields': 'id, name, email, age_range'
}

# https://apps.twitter.com/app/12803288/settings
SOCIAL_AUTH_TWITTER_KEY = 'dQemFi4fKcnUauKqrkKOyb4oL'
SOCIAL_AUTH_TWITTER_SECRET = 'RSJmTueWBzCgeK9reZ0ViE0sZXKMgi5pgiQoUfcLVCWkCM8vWU'

# https://oauth.yandex.com/
# https://oauth.yandex.com/client/edit/04d32f775cc04084b4c63ba53c763bcd
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = '04d32f775cc04084b4c63ba53c763bcd'
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = 'e98b0cc1a8c444f1859830753f42194a'

# https://www.instagram.com/developer/clients/manage/?edited=vkalendare
SOCIAL_AUTH_INSTAGRAM_KEY = '2ee6681ccb10469ab998207367bb117d'
SOCIAL_AUTH_INSTAGRAM_SECRET = '83e161fd39a64394873c81aa226153e2'
# SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

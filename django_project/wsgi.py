"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import pymysql

path = '/home/www/vkalendare.com/django_project/'
if path not in sys.path:
    sys.path.append(path)
    

pymysql.install_as_MySQLdb()


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

application = get_wsgi_application()

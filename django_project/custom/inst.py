import sys
import os
##get project directory
import pymysql
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
##get project parent directory and add to python path using sys.path.append
SYS_PATH = os.path.dirname(BASE_DIR)
if SYS_PATH not in sys.path:
    sys.path.append(SYS_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'

pymysql.install_as_MySQLdb()

django.setup()

from django_project.mysite.models import *













q = Locations.objects.get(name='Калуга')

print(q.instagram_id)
pass

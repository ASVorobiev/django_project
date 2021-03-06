#!/usr/home/www/vkalendare.com/venv/mysite/bin/python
import os
import sys

import pymysql

pymysql.install_as_MySQLdb()

import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

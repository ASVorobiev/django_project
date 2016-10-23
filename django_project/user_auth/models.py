# Define a custom User class to work with django-social-auth

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    location = models.ForeignKey('mysite.Locations', blank=True, null=True)
    pass

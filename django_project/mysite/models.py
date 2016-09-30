import hashlib
import os
import re
from django_project.user_auth.models import CustomUser
from django.db import models

from django.utils.datetime_safe import datetime
from django.utils.safestring import mark_safe
from transliterate import translit


class MysiteCategories(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mysite_categories'


class MysiteOrganizers(models.Model):
    vk_id = models.IntegerField(blank=True, null=True)
    vk_type = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    confidence = models.IntegerField()
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mysite_organizers'
        unique_together = (('vk_id', 'vk_type'),)


class MysitePlaces(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lan = models.FloatField(blank=True, null=True)
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mysite_places'

class Locations(models.Model):
    name = models.CharField(max_length=255)
    vk_group_id = models.IntegerField(blank=True, null=True)
    vk_screen_name = models.CharField(max_length=255, blank=True, null=True)
    site_screen_name = models.CharField(max_length=255, blank=True, null=True)
    vk_owner_id = models.IntegerField(blank=True, null=True)
    vk_location_event_id = models.IntegerField(blank=True, null=True)
    tz = models.IntegerField(blank=True, null=True)
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    if instance.image.name == filename:
        f = instance.image.file.file.file.getvalue()
    else:
        f = instance.thumb.file.file.file.getvalue()
    md = hashlib.md5(f).hexdigest()
    n = 2
    local_path = ''
    for dr in [md[i:i+n] for i in range(0, len(md), n)]:
        local_path = os.path.join(local_path, dr)
    local_path = os.path.join(local_path, filename)
    return local_path


class Events(models.Model):
    owner = models.ForeignKey(CustomUser, blank=True, null=True, verbose_name='Создатель')
    location = models.ForeignKey(Locations, verbose_name='Локация')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    # 'events/%Y/%m/%d'
    image = models.ImageField(max_length=255, blank=True, null=True, verbose_name='афиша', upload_to=user_directory_path)
    thumb = models.ImageField(max_length=255, blank=True, null=True, verbose_name='предпросмотр афиши', upload_to=user_directory_path)
    category_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(verbose_name='дата начала')
    start_time = models.TimeField(verbose_name='время начала')
    duration = models.IntegerField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    is_perodic = models.IntegerField(blank=True, null=True, choices=((0, 'No'), (1, 'Yes')))
    shedule = models.CharField(max_length=255, blank=True, null=True)
    # place_id = models.IntegerField(blank=True, null=True)
    place = models.ForeignKey(MysitePlaces, verbose_name='Место', blank=True, null=True, default=None)
    place_comment = models.CharField(max_length=255, blank=True, null=True)
    # organizer_id = models.IntegerField(blank=True, null=True)
    organizer = models.ForeignKey(MysiteOrganizers, verbose_name='Организатор', blank=True, null=True)
    is_free = models.IntegerField(blank=True, null=True)
    tickets = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(choices=((0, 'Обычное'),
                                            (1, 'Приоритетное')), default=0)
    is_active = models.IntegerField(choices=((9, 'Не проверено'),
                                             (0, 'Отклонено'),
                                             (1, 'Одобрено')), default=9)
    export_vk = models.IntegerField(choices=((0, 'Нет'), (1, 'Да')), default=1)
    is_deleted = models.IntegerField(choices=((0, 'Нет'), (1, 'Да')), default=0)
    created = models.IntegerField(default=int(datetime.utcnow().timestamp()))
    modified = models.IntegerField(default=int(datetime.utcnow().timestamp()))

    def image_small(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)
        else:
            return '(none)'
    image_small.short_description = 'Предпросмотр'
    image_small.allow_tags = True

    def title_translit(self):
        trans = translit(self.title.strip(), 'ru', reversed=True)
        return re.sub("[^.\w-]+", '_', trans)

    def __str__(self):
        return self.title


class LocationCities(models.Model):
    vk_city_id = models.IntegerField(primary_key=True)
    location_id = models.IntegerField()
    vk_city_name = models.CharField(max_length=255)




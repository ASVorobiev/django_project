import hashlib
import os
import re

from django.db.models import Manager
from taggit.managers import TaggableManager

from django_project.user_auth.models import CustomUser
from django.db import models, connection

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
    # is_place = models.BooleanField(default=False, blank=True)  # добавлен столбец
    confidence = models.IntegerField()
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mysite_organizers'
        unique_together = (('vk_id', 'vk_type'),)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name

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


class MyManager(Manager):
    def raw_as_qs(self, raw_query, params=()):
        """Execute a raw query and return a QuerySet.  The first column in the
        result set must be the id field for the model.
        :type raw_query: str | unicode
        :type params: tuple[T] | dict[str | unicode, T]
        :rtype: django.db.models.query.QuerySet
        """
        cursor = connection.cursor()
        try:
            cursor.execute(raw_query, params)
            return self.filter(id__in=(x[0] for x in cursor))
        finally:
            cursor.close()



class Events(models.Model):
    owner = models.ForeignKey(CustomUser, blank=True, null=True, verbose_name='Создатель')
    location = models.ForeignKey(Locations, verbose_name='Локация')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')  # strip=True
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
    # tags = models.CharField(max_length=255, blank=True, null=True)
    tag_it = TaggableManager()
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

    def clean(self):
        if self.description:
            return self.description.strip()

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

    # class loc_org(models.Field):
    #     #     description = "A hand of cards (bridge style)"
    #     #     # local_organizer = models.ForeignKey
    #     #     def __init__(self, *args, **kwargs):
    #     #         kwargs['max_length'] = 104
    #     #         super(Events, self).__init__(*args, **kwargs)
    #     #
    #     def local_organizer(self):
    #         sql_query = "SELECT * from mysite_organizers where id in (SELECT DISTINCT organizer_id from mysite_events WHERE location_id = %s) AND confidence > 1 AND vk_type = 'group' ORDER BY followers" % 1
    #         return MysiteOrganizers.objects.raw(sql_query)
    #
    #     def __str__(self):
    #         return self.name
    #
    #
    # local_organizer = loc_org().local_organizer()
    # objects = MyManager()
    # local_organizer = loc_org().local_organizer(organizer)
    # def local_organizer(self):
    #     sql_query = "SELECT * from mysite_organizers where id in (SELECT DISTINCT organizer_id from mysite_events WHERE location_id = %s) AND confidence > 1 AND vk_type = 'group' ORDER BY followers" % 1
    #     return MysiteOrganizers.objects.raw(sql_query).model
    # local_organizer.short_description = 'Организатор'
    # local_organizer.allow_tags = True

    def __str__(self):
        return self.title





class LocationCities(models.Model):
    vk_city_id = models.IntegerField(primary_key=True)
    location_id = models.IntegerField()
    vk_city_name = models.CharField(max_length=255)




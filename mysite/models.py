from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.datetime_safe import datetime
from django.utils.safestring import mark_safe

from django_project.settings import MEDIA_URL


class Person(models.Model):
    images_path = 'images/'
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=images_path, null=True, blank=True)

    def image_small(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)
        else:
            return '(none)'

    image_small.short_description = 'Thumb'
    image_small.allow_tags = True


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class Upload(models.Model):
    pic = models.ImageField("Image", upload_to=MEDIA_URL)
    upload_date = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src="/directory/%s" width="150" height="150" />' % self.pic)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'

class Locations(models.Model):
    name = models.CharField(max_length=255)
    vk_group_id = models.IntegerField(blank=True, null=True)
    vk_screen_name = models.CharField(max_length=255, blank=True, null=True)
    vk_owner_id = models.IntegerField(blank=True, null=True)
    vk_location_event_id = models.IntegerField(blank=True, null=True)
    tz = models.IntegerField(blank=True, null=True)
    is_deleted = models.IntegerField()
    modified = models.IntegerField()
    created = models.IntegerField()

    def __str__(self):
        return self.name

class Events(models.Model):
    location_id = models.ForeignKey(Locations)
    title = models.CharField(max_length=255, verbose_name='заголовок')
    description = models.TextField(blank=True, verbose_name='описание')
    image = models.ImageField(max_length=255, blank=True, null=True, verbose_name='афиша')
    thumb = models.CharField(max_length=255, blank=True, null=True, verbose_name='предпросмотр афиши')
    category_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(verbose_name='дата начала')
    start_time = models.TimeField(verbose_name='время начала')
    duration = models.IntegerField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    is_perodic = models.IntegerField(blank=True, null=True, choices=((0, 'No'), (1, 'Yes')))
    shedule = models.CharField(max_length=255, blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    place_comment = models.CharField(max_length=255, blank=True, null=True)
    organizer_id = models.IntegerField(blank=True, null=True)
    is_free = models.IntegerField(blank=True, null=True)
    tickets = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(choices=((0, 'Normal'),
                                            (1, 'Proirity')), default=0)
    is_active = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1)
    export_vk = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=1)
    is_deleted = models.IntegerField(choices=((0, 'No'), (1, 'Yes')), default=0)
    created = models.IntegerField(default=int(datetime.utcnow().timestamp()))
    modified = models.IntegerField(default=int(datetime.utcnow().timestamp()))

    def image_small(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)
        else:
            return '(none)'
    image_small.short_description = 'Thumb'
    image_small.allow_tags = True

    def __str__(self):
        return self.title


class LocationCities(models.Model):
    vk_city_id = models.IntegerField(primary_key=True)
    location_id = models.IntegerField()
    vk_city_name = models.CharField(max_length=255)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20160828_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('location_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.CharField(null=True, blank=True, max_length=255)),
                ('thumb', models.CharField(null=True, blank=True, max_length=255)),
                ('category_id', models.IntegerField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('finish_date', models.DateField(null=True, blank=True)),
                ('is_perodic', models.IntegerField(null=True, blank=True)),
                ('shedule', models.CharField(null=True, blank=True, max_length=255)),
                ('place_id', models.IntegerField(null=True, blank=True)),
                ('place_comment', models.CharField(null=True, blank=True, max_length=255)),
                ('organizer_id', models.IntegerField(null=True, blank=True)),
                ('is_free', models.IntegerField(null=True, blank=True)),
                ('tickets', models.TextField(null=True, blank=True)),
                ('tags', models.CharField(null=True, blank=True, max_length=255)),
                ('phone', models.CharField(null=True, blank=True, max_length=255)),
                ('url', models.CharField(null=True, blank=True, max_length=255)),
                ('priority', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('export_vk', models.IntegerField()),
                ('is_deleted', models.IntegerField()),
                ('modified', models.IntegerField()),
                ('created', models.IntegerField()),
            ],
        ),
    ]

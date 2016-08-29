# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_auto_20160828_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationCities',
            fields=[
                ('vk_city_id', models.IntegerField(serialize=False, primary_key=True)),
                ('location_id', models.IntegerField()),
                ('vk_city_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vk_group_id', models.IntegerField(blank=True, null=True)),
                ('vk_screen_name', models.CharField(max_length=255, blank=True, null=True)),
                ('vk_owner_id', models.IntegerField(blank=True, null=True)),
                ('vk_location_event_id', models.IntegerField(blank=True, null=True)),
                ('tz', models.IntegerField(blank=True, null=True)),
                ('is_deleted', models.IntegerField()),
                ('modified', models.IntegerField()),
                ('created', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472392648),
        ),
        migrations.AlterField(
            model_name='events',
            name='description',
            field=models.TextField(default=3, blank=True, verbose_name='описание'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(max_length=255, blank=True, upload_to='', null=True, verbose_name='афиша'),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472392648),
        ),
        migrations.AlterField(
            model_name='events',
            name='start_date',
            field=models.DateField(verbose_name='дата начала'),
        ),
        migrations.AlterField(
            model_name='events',
            name='start_time',
            field=models.TimeField(verbose_name='время начала'),
        ),
        migrations.AlterField(
            model_name='events',
            name='thumb',
            field=models.CharField(max_length=255, blank=True, null=True, verbose_name='предпросмотр афиши'),
        ),
        migrations.AlterField(
            model_name='events',
            name='title',
            field=models.CharField(max_length=255, verbose_name='заголовок'),
        ),
    ]

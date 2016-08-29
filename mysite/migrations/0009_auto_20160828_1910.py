# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20160828_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472389847),
        ),
        migrations.AlterField(
            model_name='events',
            name='export_vk',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1),
        ),
        migrations.AlterField(
            model_name='events',
            name='is_active',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1),
        ),
        migrations.AlterField(
            model_name='events',
            name='is_deleted',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AlterField(
            model_name='events',
            name='is_perodic',
            field=models.IntegerField(blank=True, null=True, choices=[(0, 'No'), (1, 'Yes')]),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472389847),
        ),
        migrations.AlterField(
            model_name='events',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Normal'), (1, 'Proirity')], default=0),
        ),
    ]

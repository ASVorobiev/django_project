# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_auto_20160828_2000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locationcities',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='locations',
            options={'managed': False},
        ),
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472392948),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472392948),
        ),
    ]

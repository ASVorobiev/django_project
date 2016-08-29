# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0017_auto_20160828_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locationcities',
            options={},
        ),
        migrations.AlterModelOptions(
            name='locations',
            options={},
        ),
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472393725),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472393725),
        ),
    ]

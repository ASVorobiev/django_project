# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0010_auto_20160828_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472392764),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472392764),
        ),
    ]

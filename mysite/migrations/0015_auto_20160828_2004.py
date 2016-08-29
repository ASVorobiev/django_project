# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0014_auto_20160828_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472393084),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472393084),
        ),
        migrations.AlterModelTable(
            name='locationcities',
            table='location_cities',
        ),
        migrations.AlterModelTable(
            name='locations',
            table='locatios',
        ),
    ]

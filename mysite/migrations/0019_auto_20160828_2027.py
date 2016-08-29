# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0018_auto_20160828_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='created',
            field=models.IntegerField(default=1472394449),
        ),
        migrations.AlterField(
            model_name='events',
            name='location_id',
            field=models.ForeignKey(to='mysite.Locations'),
        ),
        migrations.AlterField(
            model_name='events',
            name='modified',
            field=models.IntegerField(default=1472394449),
        ),
        migrations.AlterModelTable(
            name='locationcities',
            table=None,
        ),
        migrations.AlterModelTable(
            name='locations',
            table=None,
        ),
    ]

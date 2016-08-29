# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='pic',
            field=models.ImageField(verbose_name='Image', upload_to='/media/'),
        ),
    ]

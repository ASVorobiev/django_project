# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='images/', verbose_name='Image')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

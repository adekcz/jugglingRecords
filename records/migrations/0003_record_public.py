# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20161222_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 18:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findmyburritto', '0002_user_burritos_burned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='burritos_burned',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_shop_visited',
        ),
    ]

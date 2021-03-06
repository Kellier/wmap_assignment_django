# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 12:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('findmyburritto', '0003_auto_20171031_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'friends list',
                'verbose_name_plural': 'friends lists',
            },
        ),
        migrations.CreateModel(
            name='UserFriendGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('friend_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='findmyburritto.FriendGroup', verbose_name='friend group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='member')),
            ],
            options={
                'verbose_name': 'friend group members',
                'verbose_name_plural': 'friend group members',
            },
        ),
        migrations.AddField(
            model_name='friendgroup',
            name='members',
            field=models.ManyToManyField(through='findmyburritto.UserFriendGroup', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendgroup',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterUniqueTogether(
            name='userfriendgroup',
            unique_together=set([('member', 'friend_group')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 04:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0002_auto_20160810_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='downvotes',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='downvotes',
            field=models.ManyToManyField(blank=True, related_name='postDownvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='postUpvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]

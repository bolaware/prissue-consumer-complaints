# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-06 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corrfeed', '0004_auto_20160806_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corrfeed.Country'),
        ),
    ]

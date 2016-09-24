# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-24 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrfeed', '0012_auto_20160823_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority',
            name='no_of_feeds',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='authority',
            name='no_of_rf',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='authority',
            name='no_of_urf',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

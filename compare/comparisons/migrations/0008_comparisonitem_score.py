# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comparisons', '0007_auto_20160107_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparisonitem',
            name='score',
            field=models.IntegerField(default=1400),
        ),
    ]

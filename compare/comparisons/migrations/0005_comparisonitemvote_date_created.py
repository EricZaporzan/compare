# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-20 10:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comparisons', '0004_comparisonitemvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparisonitemvote',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 1, 20, 10, 27, 8, 997331, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
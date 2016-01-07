# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comparisons', '0005_comparison_date_starting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comparison',
            name='date_starting',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='When should we start?'),
        ),
    ]

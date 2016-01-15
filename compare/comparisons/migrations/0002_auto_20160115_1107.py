# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comparisons', '0001_squashed_0013_auto_20160115_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comparisonitem',
            name='comparison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comparisons.Comparison'),
        ),
        migrations.AlterField(
            model_name='comparisonitem',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'20160115160752704'),
        ),
    ]

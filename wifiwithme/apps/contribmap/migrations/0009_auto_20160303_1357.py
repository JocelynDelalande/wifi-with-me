# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribmap', '0008_remove_contrib_old_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrib',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]

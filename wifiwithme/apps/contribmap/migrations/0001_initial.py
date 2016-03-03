# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contrib',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('contrib_type', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('access_type', models.TextField(blank=True, null=True)),
                ('connect_local', models.IntegerField(blank=True, null=True)),
                ('connect_internet', models.IntegerField(blank=True, null=True)),
                ('bandwidth', models.FloatField(blank=True, null=True)),
                ('share_part', models.FloatField(blank=True, null=True)),
                ('floor', models.IntegerField(blank=True, null=True)),
                ('floor_total', models.IntegerField(blank=True, null=True)),
                ('orientations', models.TextField(blank=True, null=True)),
                ('roof', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('privacy_name', models.IntegerField(blank=True, null=True)),
                ('privacy_email', models.IntegerField(blank=True, null=True)),
                ('privacy_coordinates', models.IntegerField(blank=True, null=True)),
                ('privacy_place_details', models.IntegerField(blank=True, null=True)),
                ('privacy_comment', models.IntegerField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'contribs',
                'managed': True,
            },
        ),
    ]

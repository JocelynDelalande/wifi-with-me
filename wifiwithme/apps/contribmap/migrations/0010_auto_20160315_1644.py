# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-15 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribmap', '0009_auto_20160303_1357'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contrib',
            options={'managed': True, 'verbose_name': 'contribution'},
        ),
        migrations.AddField(
            model_name='contrib',
            name='status',
            field=models.CharField(blank=True, choices=[('A_ETUDIER', '\xe0 \xe9tudier'), ('A_CONNECTER', '\xe0 connecter'), ('CONNECTE', 'connect\xe9'), ('PAS_CONNECTABLE', 'pas connectable')], default='A_ETUDIER', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='access_type',
            field=models.CharField(blank=True, choices=[('vdsl', 'ADSL'), ('vdsl', 'VDSL'), ('fiber', 'Fibre optique'), ('cable', 'Coaxial (FTTLA)')], max_length=10, verbose_name='Type de connexion'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='bandwidth',
            field=models.FloatField(blank=True, null=True, verbose_name='d\xe9bit total'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='commentaire'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='connect_internet',
            field=models.NullBooleanField(default=False, verbose_name='Services locaux'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='connect_local',
            field=models.NullBooleanField(default=False, verbose_name='Acc\xe8s internet'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='contrib_type',
            field=models.CharField(choices=[('connect', 'Me raccorder au r\xe9seau exp\xe9rimental'), ('share', 'Partager une partie de ma connexion')], max_length=10, verbose_name='Type de contribution'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='floor',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='\xe9tage'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='floor_total',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="mombre d'\xe9tages"),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Nom / Pseudo'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='T\xe9l\xe9phone'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='privacy_comment',
            field=models.BooleanField(default=False, verbose_name='commentaire public'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='privacy_coordinates',
            field=models.BooleanField(default=True, verbose_name='coordonn\xe9es GPS publiques'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='privacy_email',
            field=models.BooleanField(default=False, verbose_name='email public'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='privacy_name',
            field=models.BooleanField(default=False, verbose_name='nom/pseudo public'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='privacy_place_details',
            field=models.BooleanField(default=True, verbose_name='\xe9tage/orientations publiques'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='roof',
            field=models.BooleanField(default=False, verbose_name='acc\xe8s au to\xeet'),
        ),
        migrations.AlterField(
            model_name='contrib',
            name='share_part',
            field=models.FloatField(blank=True, null=True, verbose_name='d\xe9bit partag\xe9'),
        ),
    ]
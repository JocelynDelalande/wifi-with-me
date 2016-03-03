from __future__ import unicode_literals

from django.db import models

from .fields import CommaSeparatedCharField


class Contrib(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=30)
    contrib_type = models.CharField(
        max_length=10, choices=(
            ('connect', 'Me raccorder au réseau expérimental'),
            ('share', 'Partager une partie de ma connexion')
        ))
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True)
    access_type = models.CharField(
        max_length=10, blank=True, choices=(
            ('vdsl', 'ADSL'),
            ('vdsl', 'VDSL'),
            ('fiber', 'Fibre optique'),
            ('cable', 'Coaxial (FTTLA)'),
        ))
    connect_local = models.NullBooleanField(default=False, null=True)
    connect_internet = models.NullBooleanField(default=False, null=True)
    bandwidth = models.FloatField(blank=True, null=True)
    share_part = models.FloatField(blank=True, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)
    floor_total = models.PositiveIntegerField(blank=True, null=True)
    orientations = CommaSeparatedCharField(
        blank=True, null=True, max_length=100)
    roof = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    privacy_name = models.BooleanField(default=False)
    privacy_email = models.BooleanField(default=False)
    privacy_coordinates = models.BooleanField(default=True)
    privacy_place_details = models.BooleanField(default=True)
    privacy_comment = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'contribs'

    def __str__(self):
        return self.name

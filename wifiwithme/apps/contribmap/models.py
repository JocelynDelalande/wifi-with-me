from __future__ import unicode_literals

from django.db import models

from .fields import CommaSeparatedCharField


class Contrib(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(
        'Nom / Pseudo',
        max_length=30)
    contrib_type = models.CharField(
        'Type de contribution',
        max_length=10, choices=(
            ('connect', 'Me raccorder au réseau expérimental'),
            ('share', 'Partager une partie de ma connexion')
        ))
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    phone = models.CharField(
        'Téléphone',
        max_length=30, blank=True, default='')
    email = models.EmailField(blank=True)
    access_type = models.CharField(
        'Type de connexion',
        max_length=10, blank=True, choices=(
            ('vdsl', 'ADSL'),
            ('vdsl', 'VDSL'),
            ('fiber', 'Fibre optique'),
            ('cable', 'Coaxial (FTTLA)'),
        ))
    connect_local = models.NullBooleanField(
        'Accès internet',
        default=False, null=True)
    connect_internet = models.NullBooleanField(
        'Services locaux',
        default=False, null=True)
    bandwidth = models.FloatField(
        'débit total',
        blank=True, null=True)
    share_part = models.FloatField(
        'débit partagé',
        blank=True, null=True)
    floor = models.PositiveIntegerField(
        'étage',
        blank=True, null=True)
    floor_total = models.PositiveIntegerField(
        "mombre d'étages",
        blank=True, null=True)
    orientations = CommaSeparatedCharField(
        blank=True, null=True, max_length=100)
    roof = models.BooleanField(
        'accès au toît',
        default=False)
    comment = models.TextField(
        'commentaire',
        blank=True, null=True)
    privacy_name = models.BooleanField(
        'nom/pseudo public',
        default=False)
    privacy_email = models.BooleanField(
        'email public',
        default=False)
    privacy_coordinates = models.BooleanField(
        'coordonnées GPS publiques',
        default=True)
    privacy_place_details = models.BooleanField(
        'étage/orientations publiques',
        default=True)
    privacy_comment = models.BooleanField(
        'commentaire public',
        default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'contribs'
        verbose_name = 'contribution'

    def __str__(self):
        return '#{} {}'.format(self.pk, self.name)

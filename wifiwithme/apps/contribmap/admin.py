# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from .models import Contrib


@admin.register(Contrib)
class ContribAdmin(admin.ModelAdmin):
    search_fields = ["name", "email", "phone"]
    list_display = ("name", "date",)

    fieldsets = [
        [None, {
            'fields': ['name', 'contrib_type'],
        }],
        ['Localisation', {
            'fields': [
                ('latitude', 'longitude'),
                ('floor', 'floor_total'),
                'orientations', 'roof']
        }],
        ['Raccordement au réseau', {
            'fields': ['connect_local', 'connect_internet'],
            'classes': ['collapse'],
        }],
        ['Partage de connexion', {
            'fields': ['access_type', 'bandwidth', 'share_part'],
            'classes': ['collapse'],
        }],
        ['Vie privée', {
            'fields': [
                'privacy_name', 'privacy_email', 'privacy_coordinates',
                'privacy_place_details', 'privacy_comment'
            ],
            'classes': ['collapse'],
        }]
    ]

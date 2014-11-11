#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname

from bottle import route, run, static_file, request, template, FormsDict

ORIENTATIONS = (
    ('N', 'Nord'),
    ('NO', 'Nord-Ouest'),
    ('O', 'Ouest'),
    ('SO', 'Sud-Ouest'),
    ('S', 'Sud'),
    ('SE', 'Sud-Est'),
    ('E', 'Est'),
    ('NE', 'Nord-Est'),
)

@route('/wifi-form')
def show_wifi_form():
    return template('wifi-form', errors=None, data = FormsDict(),
                    orientations=ORIENTATIONS)

@route('/wifi-form', method='POST')
def submit_wifi_form():
    required = ('name', 'contrib-type',
                'latitude', 'longitude')
    required_or = (('email', 'phone'),)
    required_if = (
        ('contrib-type', 'share',('access-type', 'bandwidth',
                                    'share-part')),
    )

    field_names = {
        'name'        : 'Nom/Pseudo',
        'contrib-type': 'Type de participation',
        'latitude'    : 'Localisation',
        'longitude'   : 'Localisation',
        'phone'       : 'Téléphone',
        'email'       : 'Email',
        'access-type' : 'Type de connexion',
        'bandwidth'   : 'Bande passante',
        'share-part'  : 'Débit partagé',
    }

    errors = []
    for name in required:
        if (not request.forms.get(name)):
            errors.append((field_names[name], 'ce champ est requis'))

    for name_list in required_or:
        filleds = [True for name in name_list if request.forms.get(name)]
        if len(filleds) <= 0:
            errors.append((
                    ' ou '.join([field_names[i] for i in name_list]),
                    'au moins un des de ces champs est requis'))

    for key, value, fields  in required_if:
        if request.forms.get('key') == value:
            for name in fields:
                if not request.forms.get(name):
                    errors.append(
                        (field_names[name], 'ce champ est requis'))
    if errors:
        return template('wifi-form', errors=errors, data=request.forms,
                        orientations=ORIENTATIONS)
    else:
        return 'OK'


@route('/assets/<filename:path>')
def send_asset(filename):
    return static_file(filename, root=join(dirname(__file__), 'assets'))

DEBUG = bool(os.environ.get('DEBUG', False))
run(host='localhost', port=8080, reloader=DEBUG)

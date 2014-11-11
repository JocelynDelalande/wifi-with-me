#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname

from bottle import route, run, static_file, request

form_names = {
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

@route('/wifi-form')
def show_wifi_form():
    return open('index.html').read()

@route('/wifi-form', method='POST')
def submit_wifi_form():
    required = ('name', 'contrib-type',
                'latitude', 'longitude', 'orientation')
    required_or = (('email', 'phone'),)
    required_if = (
        ('contrib-type', 'share',('access-type', 'bandwidth',
                                    'share-part')),
    )

    errors = []

    for name in required:
        if (not request.forms.get(name)):
            errors.append((name, 'Ce champ est requis'))

    for name_list in required_or:
        filleds = [True for name in name_list if request.forms.get(name)]
        if len(filleds) <= 0:
            errors.append((name_list,
                           'Au moins un des de ces champs est requis'))

    for key, value, fields  in required_if:
        if request.forms.get('key') == value:
            for name in fields:
                if not request.forms.get(name):
                    errors.append((name, 'Ce champ est requis'))
    if errors:
        return str(errors)
    else:
        return 'OK'


@route('/assets/<filename:path>')
def send_asset(filename):
    return static_file(filename, root=join(dirname(__file__), 'assets'))

DEBUG = bool(os.environ.get('DEBUG', False))
run(host='localhost', port=8080, reloader=DEBUG)

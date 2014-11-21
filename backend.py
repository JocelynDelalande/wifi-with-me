#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import urlparse
import datetime
from email import utils
from os.path import join, dirname

from bottle import route, run, static_file, request, template, FormsDict, redirect

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

TABLE_NAME = 'contribs'
DB_FILENAME = join(dirname(__file__), 'db.sqlite3')
DB = sqlite3.connect(DB_FILENAME)

DB_COLS = (
('id', 'INTEGER PRIMARY KEY'),
('name', 'TEXT'),
('contrib_type', 'TEXT'),
('latitude', 'REAL'),
('longitude', 'REAL'),
('phone', 'TEXT'),
('email', 'TEXT'),
('access_type', 'TEXT'),
('bandwidth', 'REAL'),
('share_part', 'REAL'),
('floor', 'INTEGER'),
('orientations', 'TEXT'),
('comment', 'TEXT'),
('privacy_name', 'INTEGER'),
('privacy_email', 'INTEGER'),
('privacy_coordinates', 'INTEGER'),
('privacy_place_details', 'INTEGER'),
('privacy_comment', 'INTEGER'),
('date', 'TEXT'),
)

@route('/')
def home():
     redirect("/wifi-form")

@route('/wifi-form')
def show_wifi_form():
    return template('wifi-form', errors=None, data = FormsDict(),
                    orientations=ORIENTATIONS)

def create_tabble(db, name, columns):
    col_defs = ','.join(['{} {}'.format(*i) for i in columns])
    db.execute('CREATE TABLE {} ({})'.format(name, col_defs))

def save_to_db(db, dic):
    tosave = dic.copy()
    tosave['date'] = utils.formatdate()
    return db.execute("""
INSERT INTO {}
(name, contrib_type, latitude, longitude, phone, email, access_type, bandwidth, share_part, floor, orientations, comment,
privacy_name, privacy_email, privacy_place_details, privacy_coordinates, privacy_comment, date)
VALUES (:name, :contrib_type, :latitude, :longitude, :phone, :email, :access_type, :bandwidth, :share_part, :floor, :orientations, :comment,
        :privacy_name, :privacy_email, :privacy_place_details, :privacy_coordinates, :privacy_comment, :date)
""".format(TABLE_NAME), tosave)

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
        d = request.forms
        save_to_db(DB, {
                'name'         : d.get('name'),
                'contrib_type' : d.get('contrib-type'),
                'latitude'     : d.get('latitude'),
                'longitude'    : d.get('longitude'),
                'phone'        : d.get('phone'),
                'email'        : d.get('email'),
                'phone'        : d.get('phone'),
                'access_type'          : d.get('access-type'),
                'bandwidth'            : d.get('bandwidth'),
                'share_part'           : d.get('share-part'),
                'floor'                : d.get('floor'),
                'orientations'         : ','.join(d.getall('orientation')),
                'comment'              : d.get('comment'),
                'privacy_name'         : 'name' in d.getall('privacy'),
                'privacy_email'        : 'email' in d.getall('privacy'),
                'privacy_place_details': 'details' in d.getall('privacy'),
                'privacy_coordinates'  : 'coordinates' in d.getall('privacy'),
                'privacy_comment'      : 'comment' in d.getall('privacy'),
        })
        DB.commit()
        return redirect(urlparse.urljoin(request.path,'thanks'))

@route('/thanks')
def wifi_form_thanks():
    return static_file('thanks.html',
                       root=join(dirname(__file__), 'views/'))

@route('/assets/<filename:path>')
def send_asset(filename):
    return static_file(filename, root=join(dirname(__file__), 'assets'))

DEBUG = bool(os.environ.get('DEBUG', False))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'createdb':
            create_tabble(DB, TABLE_NAME, DB_COLS)
    else:
        run(host='localhost', port=8080, reloader=DEBUG)
        DB.close()

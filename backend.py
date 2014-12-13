#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3

try:
     import urllib.parse as urlparse
except ImportError:
     # Python2
     import urlparse

import datetime
import json
from email import utils
from os.path import join, dirname


from bottle import route, run, static_file, request, template, FormsDict, redirect, response

ORIENTATIONS = (
    (u'N', u'Nord'),
    (u'NO', u'Nord-Ouest'),
    (u'O', u'Ouest'),
    (u'SO', u'Sud-Ouest'),
    (u'S', u'Sud'),
    (u'SE', u'Sud-Est'),
    (u'E', u'Est'),
    (u'NE', u'Nord-Est'),
)

TABLE_NAME = u'contribs'
DB_FILENAME = join(dirname(__file__), u'db.sqlite3')
DB = sqlite3.connect(DB_FILENAME)

DB_COLS = (
(u'id', u'INTEGER PRIMARY KEY'),
(u'name', u'TEXT'),
(u'contrib_type', u'TEXT'),
(u'latitude', u'REAL'),
(u'longitude', u'REAL'),
(u'phone', u'TEXT'),
(u'email', u'TEXT'),
(u'access_type', u'TEXT'),
(u'bandwidth', u'REAL'),
(u'share_part', u'REAL'),
(u'floor', u'INTEGER'),
(u'floor_total', u'INTEGER'),
(u'orientations', u'TEXT'),
(u'roof', u'INTEGER'),
(u'comment', u'TEXT'),
(u'privacy_name', u'INTEGER'),
(u'privacy_email', u'INTEGER'),
(u'privacy_coordinates', u'INTEGER'),
(u'privacy_place_details', u'INTEGER'),
(u'privacy_comment', u'INTEGER'),
(u'date', u'TEXT'),
)

@route(u'/')
def home():
     redirect(u"/wifi-form")

@route(u'/wifi-form')
def show_wifi_form():
    return template(u'wifi-form', errors=None, data = FormsDict(),
                    orientations=ORIENTATIONS)

def create_tabble(db, name, columns):
    col_defs = u','.join([u'{} {}'.format(*i) for i in columns])
    db.execute(u'CREATE TABLE {} ({})'.format(name, col_defs))

def save_to_db(db, dic):
    dic[u'date'] = utils.formatdate()
    return db.execute(u"""
INSERT INTO {}
(name, contrib_type, latitude, longitude, phone, email, access_type, bandwidth, share_part, floor, floor_total, orientations, roof, comment,
privacy_name, privacy_email, privacy_place_details, privacy_coordinates, privacy_comment, date)
VALUES (:name, :contrib_type, :latitude, :longitude, :phone, :email, :access_type, :bandwidth, :share_part, :floor, :floor_total, :orientations, :roof, :comment,
        :privacy_name, :privacy_email, :privacy_place_details, :privacy_coordinates, :privacy_comment, :date)
""".format(TABLE_NAME), dic)

@route(u'/wifi-form', method=u'POST')
def submit_wifi_form():
    required = (u'name', u'contrib-type',
                u'latitude', u'longitude')
    required_or = ((u'email', u'phone'),)
    required_if = (
        (u'contrib-type', u'share',(u'access-type', u'bandwidth',
                                    u'share-part')),
    )

    field_names = {
        u'name'        : u'Nom/Pseudo',
        u'contrib-type': u'Type de participation',
        u'latitude'    : u'Localisation',
        u'longitude'   : u'Localisation',
        u'phone'       : u'Téléphone',
        u'email'       : u'Email',
        u'access-type' : u'Type de connexion',
        u'bandwidth'   : u'Bande passante',
        u'share-part'  : u'Débit partagé',
        u'floor' : u'Étage',
        u'floor_total' : u'Nombre d\'étages total'
    }

    errors = []
    for name in required:
        if (not request.forms.getunicode(name)):
            errors.append((field_names[name], u'ce champ est requis'))

    for name_list in required_or:
        filleds = [True for name in name_list if request.forms.getunicode(name)]
        if len(filleds) <= 0:
            errors.append((
                    u' ou '.join([field_names[i] for i in name_list]),
                    u'au moins un des de ces champs est requis'))

    for key, value, fields  in required_if:
        if request.forms.getunicode(u'key') == value:
            for name in fields:
                if not request.forms.getunicode(name):
                    errors.append(
                        (field_names[name], u'ce champ est requis'))

    floor = request.forms.getunicode(u'floor')
    floor_total = request.forms.getunicode(u'floor_total')

    if floor and not floor_total:
        errors.append((field_names[u'floor_total'], u"ce champ est requis"))
    elif not floor and floor_total:
        errors.append((field_names[u'floor'], u"ce champ est requis"))
    elif floor and floor_total and (int(floor) > int(floor_total)):
        errors.append((field_names[u'floor'], u"Étage supérieur au nombre total"))

    if errors:
        return template(u'wifi-form', errors=errors, data=request.forms,
                        orientations=ORIENTATIONS)
    else:
        d = request.forms
        save_to_db(DB, {
                u'name'         : d.getunicode(u'name'),
                u'contrib_type' : d.getunicode(u'contrib-type'),
                u'latitude'     : d.getunicode(u'latitude'),
                u'longitude'    : d.getunicode(u'longitude'),
                u'phone'        : d.getunicode(u'phone'),
                u'email'        : d.getunicode(u'email'),
                u'phone'        : d.getunicode(u'phone'),
                u'access_type'          : d.getunicode(u'access-type'),
                u'bandwidth'            : d.getunicode(u'bandwidth'),
                u'share_part'           : d.getunicode(u'share-part'),
                u'floor'                : d.getunicode(u'floor'),
                u'floor_total'                : d.getunicode(u'floor_total'),
                u'orientations'         : u','.join(d.getall(u'orientation')),
                u'roof'         : d.getunicode(u'roof'),
                u'comment'              : d.getunicode(u'comment'),
                u'privacy_name'         : u'name' in d.getall(u'privacy'),
                u'privacy_email'        : u'email' in d.getall(u'privacy'),
                u'privacy_place_details': u'place_details' in d.getall(u'privacy'),
                u'privacy_coordinates'  : u'coordinates' in d.getall(u'privacy'),
                u'privacy_comment'      : u'comment' in d.getall(u'privacy'),
        })
        DB.commit()

        # Rebuild GeoJSON
        build_geojson()

        return redirect(urlparse.urljoin(request.path, u'thanks'))

@route(u'/thanks')
def wifi_form_thanks():
    return template(u'thanks')

@route(u'/assets/<filename:path>')
def send_asset(filename):
    return static_file(filename, root=join(dirname(__file__), u'assets'))


@route(u'/legal')
def legal():
    return template(u'legal')


"""
Results Map
"""

@route(u'/map')
def public_map():
    geojsonPath = u'public.json'
    return template(u'map', geojson=geojsonPath)

@route(u'/public.json')
def public_geojson():
    return static_file(u'public.json', root=join(dirname(__file__), u'json/'))



"""
GeoJSON Functions
"""

# Save feature collection to a json file
def save_featurecollection_json(id, features):
    with open(u'json/' + id + u'.json', u'w') as outfile:
        json.dump({
            u"type" : u"FeatureCollection",
            u"features" : features,
            u"id" : id,
        }, outfile)

# Build GeoJSON files from DB
def build_geojson():

    # Read from DB
    DB.row_factory = sqlite3.Row
    cur = DB.execute(u"""
        SELECT * FROM {} ORDER BY id DESC
        """.format(TABLE_NAME))

    public_features = []
    private_features = []

    # Loop through results
    rows = cur.fetchall()
    for row in rows:

        # Private JSON file
        private_features.append({
            u"type" : u"Feature",
            u"geometry" : {
                u"type": u"Point",
                 u"coordinates": [row['longitude'], row['latitude']],
            },
             u"id" : row['id'],
             u"properties": {
                u"name" : row['name'],
                u"place" : {
                    u'floor' : row['floor'],
                    u'floor_total' : row['floor_total'],
                    u'orientations' : row['orientations'].split(u','),
                    u'roof' : row['roof'],
                },
                u"comment" : row['comment']
             }
        })

        # Bypass non-public points
        if not row['privacy_coordinates']:
            continue

        # Public JSON file
        public_feature = {
            u"type" : "Feature",
            u"geometry" : {
                u"type": u"Point",
                u"coordinates": [row['longitude'], row['latitude']],
            },
             u"id" : row['id'],
             u"properties": {}
        }

        # Add optionnal variables
        if row['privacy_name']:
            public_feature[u'properties'][u'name'] = row['name']

        if row['privacy_comment']:
            public_feature[u'properties'][u'comment'] = row['comment']

        if row['privacy_place_details']:
            public_feature[u'properties'][u'place'] = {
                u'floor' : row['floor'],
                u'floor_total' : row['floor_total'],
                u'orientations' : row['orientations'].split(u','),
                u'roof' : row['roof'],
            }

        # Add to public features list
        public_features.append(public_feature)

    # Build GeoJSON Feature Collection
    save_featurecollection_json(u'private', private_features)
    save_featurecollection_json(u'public', public_features)



DEBUG = bool(os.environ.get(u'DEBUG', False))

if __name__ == u'__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == u'createdb':
            create_tabble(DB, TABLE_NAME, DB_COLS)
        if sys.argv[1] == u'buildgeojson':
            build_geojson()
    else:
        run(host=u'localhost', port=8080, reloader=DEBUG)
        DB.close()

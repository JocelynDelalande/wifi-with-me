#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import urlparse
import datetime
import json
from email import utils
from os.path import join, dirname


from bottle import route, run, static_file, request, template, FormsDict, redirect, response

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

# Angular sector for each direction, written as (start, stop) in degrees
ANGLES = {
     'N':  (-23, 22),
     'NO': (292, 337),
     'O':  (247, 292),
     'SO': (202, 247),
     'S':  (157, 202),
     'SE': (112, 157),
     'E':  (67, 112),
     'NE': (22, 67)
}

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
('floor_total', 'INTEGER'),
('orientations', 'TEXT'),
('roof', 'INTEGER'),
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
    # SQLite is picky about encoding else
    tosave = {bytes(k):v.decode('utf-8') if isinstance(v,str) else v for k,v in dic.items()}
    tosave['date'] = utils.formatdate()
    return db.execute("""
INSERT INTO {}
(name, contrib_type, latitude, longitude, phone, email, access_type, bandwidth, share_part, floor, floor_total, orientations, roof, comment,
privacy_name, privacy_email, privacy_place_details, privacy_coordinates, privacy_comment, date)
VALUES (:name, :contrib_type, :latitude, :longitude, :phone, :email, :access_type, :bandwidth, :share_part, :floor, :floor_total, :orientations, :roof, :comment,
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
        'floor' : 'Étage',
        'floor_total' : 'Nombre d\'étages total'
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

    floor = request.forms.get('floor')
    floor_total = request.forms.get('floor_total')

    if floor and not floor_total:
        errors.append((field_names['floor_total'], "ce champ est requis"))
    elif not floor and floor_total:
        errors.append((field_names['floor'], "ce champ est requis"))
    elif floor and floor_total and (int(floor) > int(floor_total)):
        errors.append((field_names['floor'], "Étage supérieur au nombre total"))

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
                'floor_total'                : d.get('floor_total'),
                'orientations'         : ','.join(d.getall('orientation')),
                'roof'         : d.get('roof'),
                'comment'              : d.get('comment'),
                'privacy_name'         : 'name' in d.getall('privacy'),
                'privacy_email'        : 'email' in d.getall('privacy'),
                'privacy_place_details': 'place_details' in d.getall('privacy'),
                'privacy_coordinates'  : 'coordinates' in d.getall('privacy'),
                'privacy_comment'      : 'comment' in d.getall('privacy'),
        })
        DB.commit()

        # Rebuild GeoJSON
        build_geojson()

        return redirect(urlparse.urljoin(request.path,'thanks'))

@route('/thanks')
def wifi_form_thanks():
    return template('thanks')

@route('/assets/<filename:path>')
def send_asset(filename):
    return static_file(filename, root=join(dirname(__file__), 'assets'))


@route('/legal')
def legal():
    return template('legal')


"""
Results Map
"""

@route('/map')
def public_map():
    geojsonPath = 'public.json'
    return template('map', geojson=geojsonPath)

@route('/public.json')
def public_geojson():
    return static_file('public.json', root=join(dirname(__file__), 'json/'))



"""
GeoJSON Functions
"""

# Useful for merging angle intervals (orientations)
def merge_intervals(l, wrap=360):
    """Merge a list of intervals, assuming the space is cyclic.  The
    intervals should already by sorted by start value."""
    if l == []:
        return []
    result = list()
    # Transform the 2-tuple into a 2-list to be able to modify it
    result.append(list(l[0]))
    for (start, stop) in l:
        current = result[-1]
        if start > current[1]:
            result.append([start, stop])
        else:
            result[-1][1] = max(result[-1][1], stop)
    if len(result) == 1:
        return result
    # Handle the cyclicity by merging the ends if necessary
    last = result[-1]
    first = result[0]
    if first[0] <= last[1] - wrap:
        result[-1][1] = max(result[-1][1], first[1] + wrap)
        result.pop(0)
    return result

def orientations_to_angle(orientations):
     """Return a list of (start, stop) angles from a list of orientations."""
     # Hack to make leaflet-semicircle happy (drawing a full circle only
     # works with (0, 360))
     if len(orientations) == 8:
          return [[0, 360]]
     angles = [ANGLES[orientation] for orientation in orientations]
     angles.sort(key=lambda (x, y): x)
     return merge_intervals(angles)

# Save feature collection to a json file
def save_featurecollection_json(id, features):
    with open('json/' + id + '.json', 'w') as outfile:
        json.dump({
            "type" : "FeatureCollection",
            "features" : features,
            "id" : id,
        }, outfile)

# Build GeoJSON files from DB
def build_geojson():

    # Read from DB
    DB.row_factory = sqlite3.Row
    cur = DB.execute("""
        SELECT * FROM {} ORDER BY id DESC
        """.format(TABLE_NAME))

    public_features = []
    private_features = []

    # Loop through results
    rows = cur.fetchall()
    for row in rows:
        orientations = row['orientations'].split(',')
        angles = orientations_to_angle(orientations)
        # Private JSON file
        private_features.append({
            "type" : "Feature",
            "geometry" : {
                "type": "Point",
                 "coordinates": [row['longitude'], row['latitude']],
            },
             "id" : row['id'],
             "properties": {
                "name" : row['name'],
                "place" : {
                    'floor' : row['floor'],
                    'floor_total' : row['floor_total'],
                    'orientations' : orientations,
                    'angles' : angles,
                    'roof' : row['roof'],
                },
                "comment" : row['comment']
             }
        })

        # Bypass non-public points
        if not row['privacy_coordinates']:
            continue

        # Public JSON file
        public_feature = {
            "type" : "Feature",
            "geometry" : {
                "type": "Point",
                 "coordinates": [row['longitude'], row['latitude']],
            },
             "id" : row['id'],
             "properties": {}
        }

        # Add optionnal variables
        if row['privacy_name']:
            public_feature['properties']['name'] = row['name']

        if row['privacy_comment']:
            public_feature['properties']['comment'] = row['comment']

        if row['privacy_place_details']:
            public_feature['properties']['place'] = {
                'floor' : row['floor'],
                'floor_total' : row['floor_total'],
                'orientations' : orientations,
                'angles' : angles,
                'roof' : row['roof'],
            }

        # Add to public features list
        public_features.append(public_feature)

    # Build GeoJSON Feature Collection
    save_featurecollection_json('private', private_features)
    save_featurecollection_json('public', public_features)



DEBUG = bool(os.environ.get('DEBUG', False))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'createdb':
            create_tabble(DB, TABLE_NAME, DB_COLS)
        if sys.argv[1] == 'buildgeojson':
            build_geojson()
    else:
        run(host='localhost', port=8080, reloader=DEBUG)
        DB.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import os
import sys
import sqlite3
import urlparse
import datetime
import json
from email import utils
from os.path import join, dirname, exists

import bottle
from bottle import route, run, static_file, request, template, FormsDict, redirect, response, Bottle

URL_PREFIX = os.environ.get('URL_PREFIX', '')

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
('connect_local', 'INTEGER'),
('connect_internet', 'INTEGER'),
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

GEOJSON_NAME = 'public.json'
GEOJSON_LICENSE_TYPE = 'ODC-BY'
GEOJSON_LICENSE_URL = 'http://opendatacommons.org/licenses/by/1.0/'

ANTISPAM_FIELD = 'url'

app = Bottle()

@app.route('/')
def home():
     redirect(urlparse.urljoin(request.path,join(URL_PREFIX, 'wifi-form')))

@app.route('/wifi-form')
def show_wifi_form():
    return template('wifi-form', errors=None, data = FormsDict(),
                    orientations=ORIENTATIONS, geojson=GEOJSON_NAME)

def create_tabble(db, name, columns):
    col_defs = ','.join(['{} {}'.format(*i) for i in columns])
    db.execute('CREATE TABLE {} ({})'.format(name, col_defs))

def escape(s):
     if not isinstance(s, (bool, float, int)) and (s != None):
          return cgi.escape(s)
     else:
          return s

def save_to_db(db, dic):
    # SQLite is picky about encoding else
    tosave = {bytes(k):escape(v.decode('utf-8')) if isinstance(v,str)
              else escape(v)
              for k,v in dic.items()}
    tosave['date'] = utils.formatdate()
    return db.execute("""
INSERT INTO {}
(name, contrib_type, latitude, longitude, phone, email, access_type, connect_local, connect_internet, bandwidth, share_part, floor, floor_total, orientations, roof, comment,
privacy_name, privacy_email, privacy_place_details, privacy_coordinates, privacy_comment, date)
VALUES (:name, :contrib_type, :latitude, :longitude, :phone, :email, :access_type, :connect_local, :connect_internet, :bandwidth, :share_part, :floor, :floor_total, :orientations, :roof, :comment,
        :privacy_name, :privacy_email, :privacy_place_details, :privacy_coordinates, :privacy_comment, :date)
""".format(TABLE_NAME), tosave)

@app.route('/wifi-form', method='POST')
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

    if request.forms.get(ANTISPAM_FIELD):
         errors.append(('', "Une erreur s'est produite"))

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
        if request.forms.get(key) == value:
            for name in fields:
                if not request.forms.get(name):
                    errors.append(
                        (field_names[name], 'ce champ est requis'))

    floor = request.forms.get('floor')
    floor_total = request.forms.get('floor_total')

    if floor and not floor_total:
        errors.append((field_names['floor_total'], "ce champ est requis"))
    if not floor and floor_total:
        errors.append((field_names['floor'], "ce champ est requis"))
    if floor and floor_total and (int(floor) > int(floor_total)):
        errors.append((field_names['floor'], "Étage supérieur au nombre total"))
    if floor and (int(floor) < 0):
        errors.append((field_names['floor'], "l'étage doit-être positif"))
    if floor_total and (int(floor_total) < 0):
        errors.append((field_names['floor_total'], "le nombre d'étages doit-être positif"))

    if errors:
        return template('wifi-form', errors=errors, data=request.forms,
                        orientations=ORIENTATIONS, geojson=GEOJSON_NAME)
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
                'connect_local'        : 'local' in d.getall('connect-type'),
                'connect_internet'     : 'internet' in d.getall('connect-type'),
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

        return redirect(urlparse.urljoin(request.path,join(URL_PREFIX,'thanks')))

@app.route('/thanks')
def wifi_form_thanks():
    return template('thanks')

@app.route('/assets/<filename:path>')
def send_asset(filename):
     for i in STATIC_DIRS:
          path = join(i, filename)
          if exists(path):
               return static_file(filename, root=i)
     raise bottle.HTTPError(404)

@app.route('/legal')
def legal():
    return template('legal')


"""
Results Map
"""

@app.route('/map')
def public_map():
    return template('map', geojson=GEOJSON_NAME)

@app.route('/public.json')
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
     # Cleanup
     orientations = [o for o in orientations if o in ANGLES.keys()]
     # Hack to make leaflet-semicircle happy (drawing a full circle only
     # works with (0, 360))
     if len(orientations) == 8:
          return [[0, 360]]
     angles = [ANGLES[orientation] for orientation in orientations]
     angles.sort(key=lambda (x, y): x)
     return merge_intervals(angles)

# Save feature collection to a json file
def save_featurecollection_json(id, features, licenses = None):
    with open('json/' + id + '.json', 'w') as outfile:
        if licenses == None:
            json.dump({
                "type" : "FeatureCollection",
                "features" : features,
                "id" : id,
            }, outfile)
        else:
             json.dump({
                "type" : "FeatureCollection",
                "features" : features,
                "id" : id,
                "licenses" : licenses,
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
        if row['roof'] == "on":
             angles = [(0, 360)]
        else:
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
                    'contrib_type' : row['contrib_type']
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
             "properties": {'contrib_type': row['contrib_type']}
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
    public_json_licenses = {
        "type" : GEOJSON_LICENSE_TYPE,
        "url" : GEOJSON_LICENSE_URL
    }
    save_featurecollection_json('public', public_features, public_json_licenses)



DEBUG = bool(os.environ.get('DEBUG', False))
LISTEN_ADDR= os.environ.get('BIND_ADDR', 'localhost')
LISTEN_PORT= int(os.environ.get('BIND_PORT', 8080))
URL_PREFIX = os.environ.get('URL_PREFIX', '').strip('/')
CUSTOMIZATION_DIR = os.environ.get('CUSTOMIZATION_DIR', None)
STATIC_DIRS = [join(dirname(__file__), 'assets')]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'createdb':
            create_tabble(DB, TABLE_NAME, DB_COLS)
        if sys.argv[1] == 'buildgeojson':
            build_geojson()
    else:
        if URL_PREFIX:
            print('Using url prefix "{}"'.format(URL_PREFIX))
            root_app = Bottle()
            root_app.mount('/{}/'.format(URL_PREFIX), app)
            run(root_app, host=LISTEN_ADDR, port=LISTEN_PORT, reloader=DEBUG)

        if CUSTOMIZATION_DIR:
             custom_templates_dir = join(CUSTOMIZATION_DIR, 'views')
             if exists(custom_templates_dir):
                 bottle.TEMPLATE_PATH.insert(0, custom_templates_dir)
             custom_assets_dir = join(CUSTOMIZATION_DIR, 'assets')
             if exists(custom_assets_dir):
                 STATIC_DIRS.insert(0, custom_assets_dir)

        run(app, host=LISTEN_ADDR, port=LISTEN_PORT, reloader=DEBUG)
        DB.close()

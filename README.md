Dependencies
============
We use bottle micro-framework.


     # apt-get install python-bottle

(current code works with debian-stable version of bottle)

or

    $ pip install bottle

Running
=======

    $ ./backend.py


Then hit *http://localhost:8080*

To run in debug mode (auto-reload)

    $ DEBUG=1 ./backend.py

Bottle will reload on source change, but not on template change if you're using
an old version of bottle.

Create the DataBase
===================

    $ python backend.py createdb

Build GeoJSON files
===================

    $ python backend.py buildgeojson

Drop the database
=================

    $ rm db.sqlite3

What else ?

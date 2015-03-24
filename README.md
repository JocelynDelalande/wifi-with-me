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

You can specify listening port and address by setting `BIND_PORT` and
`BIND_ADDR` env vars, ex:

    BIND_ADDR='0.0.0.0' BIND_PORT=8081 ./backend.py

Default is to listen on `127.0.0.0`, port `8080`.

You can also pass a `URL_PREFIX='/some_folder/'` if you don't want the app to be
served at the root of the domain.

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

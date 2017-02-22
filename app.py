#!flask/bin/python
#########!/usr/bin/env python

from flask import Flask, jsonify
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from ext import db,migrate,cache
#
from views import main_blueprint
from views import root_blueprint

import models

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    cache.init_app(app,config={
           'CACHE_TYPE': 'memcached',
           'CACHE_MEMCACHED_SERVERS': app.config['CACHE_MEMCACHED_SERVERS']
       })
    app.register_blueprint(main_blueprint)
    app.register_blueprint(root_blueprint)
    app.secret_key = 'super secret key'
    app.secret_key = app.config['SESSION_KEY']
    migrate.init_app(app,db)
    db.init_app(app)
    return app


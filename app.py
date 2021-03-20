#!/usr/bin/python3

import sqlite3
import sys, configparser, json
from flask import Flask, request, abort, render_template, g
from functools import wraps
from waitress import serve
import os

# --------- Database ---------
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            database,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# --------- Global Configs ---------
configparser = configparser.ConfigParser()

if(os.getenv('APP_ENV') == 'production'):
    configparser.read('/app/config.ini') # Docker
else:
    configparser.read('config.ini') # Local

host = configparser['Server']['host']
port = configparser['Server']['port']
database = configparser['Server']['database']
api_endpoint = configparser['Api']['endpoint']

# --------- App Configs ---------
app = Flask(__name__, instance_relative_config=False)

if(os.getenv('APP_ENV') == 'production'):
    app.config.from_pyfile('/app/config.py')
else:
    app.config.from_pyfile('config.py')

app.teardown_appcontext(close_db)

# --------- Errors ---------
@app.errorhandler(400)
def bad_request(r):
    return {'error': '%s' % r.description}, 400


@app.errorhandler(401)
def unauthorized(r):
    return {'error': '%s' % r.description}, 401


@app.errorhandler(404)
def not_found(r):
    return {'error': '%s' % r.description}, 404


@app.errorhandler(405)
def method_not_allowed(r):
    return {'error': '%s' % r.description}, 405


@app.errorhandler(500)
def internal_server_error(r):
    return {'error': '%s' % r.description}, 500

# --------- Routes ---------
@app.route('/oracle', methods=['GET'])
def home():

    try:
        con = get_db()
    except Error as e:
        return abort(500, 'No database connection')

    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM gas_fees")
        data = cur.fetchall()

    return {}

if __name__ == '__main__':
    serve(app, host=host, port=port)


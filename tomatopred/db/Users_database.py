import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


DATABASE = os.path.join(os.getcwd(),'tomatopredict','data','Users_database.db')

def create_usertable():
	co = sqlite3.connect(DATABASE)
	c = co.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS userstable(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,password TEXT, email TEXT)')
	c.close()



import sqlite3
from flask import g
import os

from flask.app import Flask

app = Flask(__name__)
DATABASE = os.path.join(os.getcwd(),'tomatopred','data','data.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
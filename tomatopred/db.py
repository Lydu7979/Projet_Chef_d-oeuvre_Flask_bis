import sqlite3
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
import os


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

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()
    
@app.cli.command('init_db')
def init_db_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)

from flask import Flask, redirect, render_template, flash, url_for
import flask_monitoringdashboard as dashboard
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_migrate import Migrate
#from flask_jwt_extended import JWTManager
#from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
import os
import sqlite3
from flask import g



app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never_guess'



DATABASE = os.path.join(os.getcwd(),'tomatopredict','data','data.db')

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

import views

"""db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
jwt = JWTManager()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    initialize_extensions(app)
    #register_blueprints(app)
    dashboard.bind(app)
    return app

def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)"""


    
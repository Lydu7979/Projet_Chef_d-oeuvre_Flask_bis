
from flask import Flask, redirect, render_template, flash, url_for, g
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
import sys
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')
import tomatopred.views
import config

db = SQLAlchemy()
bcrypt = Bcrypt()
# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
mail = Mail()
#migrate = Migrate()
#jwt = JWTManager()
# login = LoginManager()


DATABASE = os.path.join(os.getcwd(),'tomatopred','data','data.db')


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    bcrypt.init_app(app)
    # login_manager.init_app(app)
    mail.init_app(app)
    register_blueprint(app)

    
    # dashboard.bind(app)

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return app

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def register_blueprint(app):
    from tomatopred.views import tomatoapp
    
    app.register_blueprint(tomatoapp)
    


    
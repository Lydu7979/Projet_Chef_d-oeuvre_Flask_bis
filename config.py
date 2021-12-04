from flask import Flask, redirect, render_template, flash, url_for
import flask_monitoringdashboard as dashboard
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
import os

SECRET_KEY = os.environ("SECRET_KEY")
MAIL_USERNAME = os.environ("MAIL_USERNAME")
MAIL_PASSWORD = os.environ("MAIL_PASSWORD")

ADMIN_USERNAME = os.environ('ADMIN_USERNAME')
ADMIN_EMAIL = os.environ('ADMIN_EMAIL')
ADMIN_PASSWORD = os.environ('ADMIN_PASSWORD')
ADMIN_ACCESS = os.environ('ADMIN_ACCESS')

class Baseconfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ('MAIL_PASSWORD') 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopementConfig(Baseconfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ('DEVELOPMENT_DATABASE_URI')
    LOGIN_DISABLED = False

class TestingConfig(Baseconfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ('TESTING_DATABASE_URI')
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    #SESSION_COOKIE_SECURE = False
    

class ProductionConfig(Baseconfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ('PRODUCTION_DATABASE_URI')

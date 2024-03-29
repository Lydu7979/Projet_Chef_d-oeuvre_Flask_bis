import sys
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')
sys.path.append('/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')

from flask import Flask, request, session
import flask_monitoringdashboard as d
import os

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(os.getcwd(),'tomatopred','data','data.db')
    app.secret_key = 'xyzdrrrretetetetetete'
    #d.config.init_from(file='/Projet_Chef_d-oeuvre_Flask_bis/tomatopred/configt.cfg')
    #d.config.group_by = lambda : 8
    # print(request.environ['REMOTE_ADDR'])
    d.bind(app)
    from . import db
    db.init_app(app)

    from . import auth, index, application, dataviz, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(application.bp)
    app.register_blueprint(dataviz.bp)
    app.register_blueprint(dashboard.bp)
    


    return app
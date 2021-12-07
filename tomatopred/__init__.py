
from flask import Flask

import os




def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(os.getcwd(),'tomatopred','data','data.db')
    app.secret_key = 'xyzdrrrretetetetetete'
    from . import db
    db.init_app(app)

    from . import auth, index, application, dataviz
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(application.bp)
    app.register_blueprint(dataviz.bp)
    


    return app
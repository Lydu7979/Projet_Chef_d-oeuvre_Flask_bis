import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm
from tomatopred.db import get_db
import logging
import pandas as pd
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')
from flask_login import login_required, current_user
import super_user

bp = Blueprint('dashboardad',__name__)

@bp.route('/dashboard', methods = ['GET', 'POST'])
def admin_user():
    if request.method =='GET':
        db = get_db()#récupération de la base de données "data.db"
        users = pd.DataFrame()#retour la liste des utilisateurs  
        try:
            users = pd.read_sql_query("SELECT usertable.id, usertable.username, usertable.email, prediction.pred_prix, prediction.pred_pro FROM usertable LEFT JOIN prediction ON usertable.id = prediction.id_user ORDER BY usertable.id;", db)
            print(users)
        except Exception as e:
            logging.error(e)


    return render_template('dashboard.html', users  = users.to_html())

@bp.route('/dashboard', methods=('GET', 'POST'))
def admin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        if email == super_user.super_login_email and password == super_user.super_pwd:
            users = pd.DataFrame()
            users = pd.read_sql_query("SELECT usertable.id, usertable.username, usertable.email, prediction.pred_prix, prediction.pred_pro FROM usertable LEFT JOIN prediction ON usertable.id = prediction.id_user ORDER BY usertable.id;", db)

    return render_template('admin/dashboard.html', users  = users.to_html())



# @bp.route('/dash')
# def dash():
#     if not current_user.admin_user():
#         return render_template('403.html')
#     return redirect('http://localhost:5000/dashboard/overview')


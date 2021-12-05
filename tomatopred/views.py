from tomatopred.db import get_db
from flask import request, render_template, redirect, url_for, flash, Flask, Blueprint
from forms import RegisterForm, LoginForm
from tomatopred.utils import data_viz_1
from tomatopred.utils.MG import mg
from tomatopred.utils.arima import prix_a, pro_a, graph_prix_ARIMA1, graph_prix_ARIMA2, graph_pro_ARIMA1, graph_pro_ARIMA2, predict_prix_ARIMA, predict_production_ARIMA
from tomatopred.utils.lstm import pred_prix_lstm, pred_pro_lstm, graph_price_lstm, table_price_lstm, graph_prod_lstm,  table_prod_lstm
from tomatopred import db
import sqlite3
import os


tomatoapp = Blueprint('tomatoapp',__name__)

# @tomatoapp.before_app_first_request
# def create_db():
#     DATABASE = os.path.join(os.getcwd(),'tomatopred','data','data.db')
#     co = sqlite3.connect(DATABASE)
#     c = co.cursor()
#     c.execute('CREATE TABLE IF NOT EXISTS userstable(id INTEGER, username TEXT,password TEXT, email TEXT, PRIMARY KEY(id))')
#     c.close()


@tomatoapp.route("/")
def index():
    cur = get_db().cursor()
    print(cur)
    return render_template('base.html')


@tomatoapp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('tomatoapp.application'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("signin.html", form=form)


@tomatoapp.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Thanks for registering')
        return redirect(url_for('signin'))
    return render_template('signup.html', form =form)

'''@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('base'))'''


@tomatoapp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@tomatoapp.route('/application')
def application():
    g1 = data_viz_1.graph_u()
    return render_template('application.html', graph = g1)

@tomatoapp.route('/data-viz', methods = ['GET', 'POST'])
def essai():
    nbd = request.form.get('nbd')
    #arima
    tabprixa = prix_a(int(nbd))
    print(tabprixa)
    tabproa = pro_a(int(nbd))
    print(tabproa)
    graph_pricea1 = graph_prix_ARIMA1(tabprixa)
    graph_pricea2 = graph_prix_ARIMA2(tabprixa)
    graph_proda1 = graph_pro_ARIMA1(tabproa)
    graph_proda2 = graph_pro_ARIMA2(tabproa)
    tapricea = predict_prix_ARIMA(tabprixa)
    taproda = predict_production_ARIMA(tabproa)
    #lstm
    # tabprixl = pred_prix_lstm(int(nbd))
    # tabprol = pred_pro_lstm(int(nbd))
    # print(tabprixl)
    # tpril= table_price_lstm(tabprixl)
    # gpril = graph_price_lstm(tabprixl)
    # tprol = table_prod_lstm(tabprol)
    # gprol = graph_prod_lstm(tabprol)
    optradio1 = request.form.get('optradio1')
    print(optradio1)
    optradio2 = request.form.get('optradio2')
    print(optradio2)
    optradio3 = request.form.get('optradio3')
    print(optradio3)
    optradio11 = request.form.get('optradio11')
    print(optradio11)
    optradio12 = request.form.get('optradio12')
    print(optradio12)
    optradio13 = request.form.get('optradio13')
    print(optradio13)
    optradio14 = request.form.get('optradio14')
    print(optradio14)
    optradio15 = request.form.get('optradio15')
    print(optradio15)
    optradio16 = request.form.get('optradio16')
    print(optradio16)
    # optradio21 = request.form.get('optradio21')
    # print(optradio21)
    # optradio22 = request.form.get('optradio22')
    # print(optradio22)
    # optradio23 = request.form.get('optradio23')
    # print(optradio23)
    # optradio24 = request.form.get('optradio24')
    # print(optradio24)
    global g1
    if optradio1 == "on":
        g1 = data_viz_1.graph_u()
    elif optradio2 == "on":
        g1 = data_viz_1.graph_prix()
    elif optradio3 == "on":
        g1 = data_viz_1.graph_pro()
    elif optradio11 == "on":
        tabprix = tapricea
    elif optradio12 == "on":
        g1 = graph_pricea1
    elif optradio13 == "on":
        g1 = graph_pricea2
    elif optradio14 == "on":
        tabpro = taproda
    elif optradio15 == "on":
        g1 = graph_proda1
    elif optradio16 == "on":
        g1 = graph_proda2
    # elif optradio21 == "on":
    #     tabprix =  tpril
    # elif optradio22 == "on":
    #     g1 = gpril
    # elif optradio23 == "on":
    #     tabpro = tprol
    # elif optradio24 == "on":
    #     g1 = gprol   
    else:
        return render_template('application.html', graph = "Nok", flag = "Nok")
    return render_template('application.html', graph = g1, table_prix = tabprix.to_html() , table_prod = tabpro.to_html())
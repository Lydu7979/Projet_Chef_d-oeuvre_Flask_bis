import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm
from tomatopred.db import get_db
from tomatopred.utils.data_viz_1 import graph_u, graph_prix, graph_pro
from tomatopred.utils.MG import mg
from tomatopred.utils.arima import prix_a, pro_a, graph_prix_ARIMA1, graph_prix_ARIMA2, graph_pro_ARIMA1, graph_pro_ARIMA2, predict_prix_ARIMA, predict_production_ARIMA
import logging
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')
from tomatopred.db import get_db

bp = Blueprint('tomatoappdataviz',__name__)

@bp.route('/data-viz', methods = ['GET', 'POST'])
def essai():
    nbd = request.form.get('nbd')
    print(session.get('user_id'))
    logging.info('Choose a number of days between 1 and 30')
    #arima
    tabprixa = prix_a(int(nbd))
    tabproa = pro_a(int(nbd))
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
    logging.info('Click a point to see a graph or a table')
    optradio1 = request.form.get('optradio1')
    optradio2 = request.form.get('optradio2')
    optradio3 = request.form.get('optradio3')
    optradio11 = request.form.get('optradio11')
    optradio12 = request.form.get('optradio12')
    optradio13 = request.form.get('optradio13')
    optradio14 = request.form.get('optradio14')
    optradio15 = request.form.get('optradio15')
    optradio16 = request.form.get('optradio16')
    # optradio21 = request.form.get('optradio21')
    # print(optradio21)
    # optradio22 = request.form.get('optradio22')
    # print(optradio22)
    # optradio23 = request.form.get('optradio23')
    # print(optradio23)
    # optradio24 = request.form.get('optradio24')
    # print(optradio24)
    if optradio1 == "on":
        g1 = graph_u()
    elif optradio2 == "on":
        g1 = graph_prix()
    elif optradio3 == "on":
        g1 = graph_pro()
    elif optradio11 == "on":
        g1 = tapricea
    elif optradio12 == "on":
        g1 = graph_pricea1
    elif optradio13 == "on":
        g1 = graph_pricea2
    elif optradio14 == "on":
        g1 = taproda
    elif optradio15 == "on":
        g1 = graph_proda1
    elif optradio16 == "on":
        g1 = graph_proda2
    # elif optradio21 == "on":
    #     t1 =  tpril
    # elif optradio22 == "on":
    #     g1 = gpril
    # elif optradio23 == "on":
    #     t2 = tprol
    # elif optradio24 == "on":
    #     g1 = gprol   
    else:
        return render_template('application.html', graph = "Nok", flag = "Nok")
    
    savedata(tapricea, taproda)

    return render_template('application.html', graph = g1)

def savedata(tapricea, taproda):
    u = session.get('user_id')
    print(u)
    db = get_db()
    db.execute("INSERT INTO prediction (id_user, id_models, pred_prix , pred_pro) VALUES (?, ?, ?, ?)",
        (u, 1, tapricea, taproda),
    )
    db.commit()




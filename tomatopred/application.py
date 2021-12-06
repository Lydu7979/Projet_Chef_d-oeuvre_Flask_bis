import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm
from tomatopred.db import get_db
from tomatopred.utils import data_viz_1
from tomatopred.utils.MG import mg
from tomatopred.utils.arima import prix_a, pro_a, graph_prix_ARIMA1, graph_prix_ARIMA2, graph_pro_ARIMA1, graph_pro_ARIMA2, predict_prix_ARIMA, predict_production_ARIMA


bp = Blueprint('tomatoapp',__name__)

@bp.route('/application')
def application():
    g1 = data_viz_1.graph_u()
    return render_template('application.html', graph = g1)
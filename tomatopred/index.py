import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm
from tomatopred.db import get_db

bp = Blueprint('tomatoappindex',__name__)

@bp.route("/")
def index():
    cur = get_db().cursor()
    print(cur)
    return render_template('index.html')
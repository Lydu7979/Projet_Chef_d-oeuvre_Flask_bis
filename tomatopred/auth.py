import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm
from tomatopred.db import get_db
import logging
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
            logging.error('Username is required.')
        elif not password:
            error = 'Password is required.'
            logging.error('Password is required.')
        elif not email:
            error = 'Email is required.'
            logging.error('Email is required.')

        if error is None:
            try:
                db.execute(
                    "INSERT INTO usertable (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
                logging.error('User already registered.')
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', form =form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM usertable WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
            logging.warning('Put a correct username')
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            logging.warning('Put a correct password')

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('tomatoapp.application'))

        flash(error)

    return render_template('auth/login.html', form =form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usertable WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
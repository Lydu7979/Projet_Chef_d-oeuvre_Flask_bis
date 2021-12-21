from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm
from tomatopred.db import get_db
from flask_login import login_required, current_user
import logging
import pandas as pd
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')
from flask_login import login_required, current_user



def users_id(user_id):
    db = get_db()
    user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
    
    return user




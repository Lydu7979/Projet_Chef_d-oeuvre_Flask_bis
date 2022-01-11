import sys
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')
sys.path.append('/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')

from tomatopred import create_app ,db
import pytest
import os
from tomatopred.models import UserModel



@pytest.fixture(scope='module')
def new_user():
    user = UserModel('usertest@yahoo.com', 'FlaskIsAwesome')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
 
    
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  
 
    ctx.pop()

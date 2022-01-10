import sys
print(sys.path)
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/tomatopred')
sys.path.append('/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/tomatopred')

import pytest
from tomatopred.utils.arima import prix_a, pro_a, graph_prix_ARIMA1, graph_prix_ARIMA2, graph_pro_ARIMA1, graph_pro_ARIMA2, predict_prix_ARIMA, predict_production_ARIMA
# from app import create_app, db
# from app.models import UserModel
# from config import TestingConfig
from tomatopred.auth import login
import os
import pandas as pd
from tests.conftest import test_client
from snapshottest_ext.dataframe  import PandasSnapshot

# @pytest.fixture(scope='module')
# def new_user():
#     user = UserModel('usertest@yahoo.fr', 'Prediction1')
#     return user

# @pytest.fixture(scope='module')
# def test_client():
#     appli = create_app(TestingConfig)
#     test_client = appli.test_client()
#     ct = appli.app_context()
#     ct.push()
 
#     yield test_client

# @pytest.fixture(scope='module')
# def database(test_client):
    
#     db.create_all()
 
#     user1 = UserModel(email='usertest@yahoo.com',username='Usertesty',plaintext_password='Prediction1')
#     user2 = UserModel(email='usertest@gmail.com',username='Usertestg',plaintext_password='Dewynteratyay')
#     #user1.set_password(text_password='Prediction1')
#     #user2.set_password(text_password='Dewynteratyay')
#     db.session.add(user1)
#     db.session.add(user2)
 
    
#     db.session.commit()
 
#     yield  
 
#     db.drop_all()

# @pytest.fixture(scope='function')
# def login_default_user(test_client):
#     test_client.post('/login',
#                      data=dict(email='usertest@yahoo.com', password='Prediction1'),
#                      follow_redirects=True)

#     yield  

#     test_client.get('/logout', follow_redirects=True)

def test_la():
    nbd = 1
    assert nbd == 1, "Error"

def test_prixa():
     nbd = 7
     print(prix_a(nbd))
     assert isinstance(prix_a(nbd),pd.DataFrame) is True #pour vérifier qu'il s'agit bien d'un dataframe

def test_proa():
     nbd = 7
     print(pro_a(nbd))
     assert isinstance(pro_a(nbd),pd.DataFrame) is True

def test_prixa2():
     nbd = 7
     prix_a(nbd)
     assert prix_a(nbd).all().all(), True #pour vérifier si toutes les valeurs du dataframe existent

def test_pro2():
     nbd = 7
     pro_a(nbd)
     assert pro_a(nbd).all().all(), True

def test_prixa3(snapshot):
     nbd = 7
     prix_a(nbd)
     snapshot.assert_match(PandasSnapshot(prix_a(nbd)))

def test_proa3(snapshot):
     nbd = 7
     pro_a(nbd)
     snapshot.assert_match(PandasSnapshot(prix_a(nbd)))


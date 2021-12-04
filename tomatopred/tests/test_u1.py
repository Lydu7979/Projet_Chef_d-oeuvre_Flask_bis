import pytest
from app import create_app, db
from app.models import UserModel
from config import TestingConfig


@pytest.fixture(scope='module')
def new_user():
    user = UserModel('usertest@yahoo.fr', 'Prediction1')
    return user

@pytest.fixture(scope='module')
def test_client():
    appli = create_app(TestingConfig)
    test_client = appli.test_client()
    ct = appli.app_context()
    ct.push()
 
    yield test_client

@pytest.fixture(scope='module')
def database(test_client):
    
    db.create_all()
 
    user1 = UserModel(email='usertest@yahoo.com',username='Usertesty',plaintext_password='Prediction1')
    user2 = UserModel(email='usertest@gmail.com',username='Usertestg',plaintext_password='Dewynteratyay')
    #user1.set_password(text_password='Prediction1')
    #user2.set_password(text_password='Dewynteratyay')
    db.session.add(user1)
    db.session.add(user2)
 
    
    db.session.commit()
 
    yield  
 
    db.drop_all()

@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='usertest@yahoo.com', password='Prediction1'),
                     follow_redirects=True)

    yield  

    test_client.get('/logout', follow_redirects=True)

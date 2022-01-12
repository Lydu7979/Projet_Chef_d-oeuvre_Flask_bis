import sys
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')
sys.path.append('/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')


def test_login_page(test_client):
    response = test_client.get('/auth/login')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' in response.data

def test_register_page(test_client):
    response = test_client.get('/auth/register')
    assert response.status_code == 200
    assert b'username' in response.data
    assert b'email' in response.data
    assert b'password' in response.data

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Sign up' in response.data
    assert b'Sign in' in response.data
    assert b'Application' in response.data
    assert b'future' in response.data

def test_user_register(test_client):
    response = test_client.post('/auth/register',
                                data=dict(Username='Usertest',
                                          email='utest@gmail.com',
                                          password='FlaskI45454',
                                          confirm='FlaskI45454'),
                                follow_redirects=True)
    assert response.status_code == 200
    
    


def test_user_login(test_client):
    response = test_client.post('/auth/login',
                                data=dict(
                                          email='utest@gmail.com',
                                          password='FlaskI45454',
                                          ),
                                follow_redirects=True)
    assert response.status_code == 200
    

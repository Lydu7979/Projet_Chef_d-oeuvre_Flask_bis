from tomatopred.__init__ import create_app
import tomatopred
import pytest
import os
import sys
print(sys.path)
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/tomatopred')
sys.path.append('/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/tomatopred')

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  
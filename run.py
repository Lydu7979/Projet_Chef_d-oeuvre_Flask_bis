import sys
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')
from tomatopred import create_app
import config


app = create_app(config.Baseconfig)

if __name__ == '__main__':
    app.run(debug=True)
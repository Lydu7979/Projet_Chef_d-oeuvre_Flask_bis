#from app import db
"""print('Hello')
import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for, send_file, flash 
from pathlib import Path
import os.path
import pytest
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import matplotlib.pyplot as plt
import warnings                                  
warnings.filterwarnings('ignore')
from datetime import date
import base64 
import time
timestr = time.strftime("%Y%m%d")
from Sécurité.Safe import modi, verif
from sklearn.preprocessing import MinMaxScaler
import pickle
import datetime 
from Pages_db.Admin import admin
from app import db
from Base_données.DBMongo import get_client_mongodb
import dns
import pymongo
from keras.models import load_model
"""

app = Flask(__name__)
"""
n = input("Choisir le nombre de jours pour les prédictions, entre 1 et 30:")
period = int(n)

mod = pickle.load(open('modèle_ARIMA_Prix3.pkl', 'rb'))
			
mod2 = pickle.load(open('modèle_ARIMA_Production3.pkl', 'rb'))

mod3 = load_model('prediction_prix_tomate_lstm_model_v1.h5')

mod4 = load_model('prediction_production_tomate_lstm_model_v1.h5')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<user>.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'xyzdrrrretetetetetete'

client = get_client_mongodb()

db2 = client.Tomates_meteo_Centre8
mycl = db2["données"]
Dat = pd.DataFrame(list(mycl.find()))
Dat = Dat.drop(columns=["index"])
print(Dat) #pour afficher la base de données sous forme de dataframe
DT = pd.DataFrame(Dat, columns = ['Date', 'prix moyen au kg', 'Production quantité \ntonne(s)', 'Température minimale en °C', 
                              'Température maximale en °C', 'précipitations en mm','Ensoleillement en min', 'Rafales (vitesse du vent) en km/h','catégorie tomates'])
DT.rename(columns={"Production quantité \ntonne(s)": "Production quantité tonne(s)"},inplace=True)
DT.to_csv('DATA/TMN.csv',index = False)

Pop = pd.read_csv("/Data/TMN.csv", parse_dates=['Date'], dayfirst= True)
Pop.sort_values(by=['Date'], inplace=True, ascending=True) 
Pop = Pop.set_index(['Date'])
Pop2 = Pop.resample("D").mean()
Pop2 = Pop2.interpolate()
Pop3 = Pop2[['prix moyen au kg','Production quantité tonne(s)']] 
print(Pop3)


scaler = MinMaxScaler()
				
Pop3[['prix_n', 'production_n']] = scaler.fit_transform(Pop3[['prix moyen au kg', 'Production quantité tonne(s)']])

data = Pop3.filter(['prix moyen au kg'])
data2 = Pop3.filter(['Production quantité tonne(s)'])

#pour l'arima

#prix
forecast,err,ci = mod.forecast(steps= period, alpha = 0.05)
nprix = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'), 'prix dans '+ str(n) +" "+'jours' :list(forecast)})
df_forecast = pd.DataFrame({'Prix dans '+  str(n) +" "+'jours' :forecast},index=pd.date_range(start=datetime.date.today(), periods=period, freq='D'))
df_forecast.to_csv("Forecast.csv")
forcast=pd.read_csv('Forecast.csv')	
forcast.rename(columns={"Unnamed: 0": "Date",'Prix dans '+ str(n) +" "+'jours':"prix moyen au kg"},inplace=True)
forcast['Date'] = pd.to_datetime(forcast['Date'],infer_datetime_format=True)
forcast.index=forcast['Date']
del forcast['Date']
fig1 = pd.concat([data,forcast])

#production
forecast2,err,ci = mod2.forecast(steps= period, alpha = 0.05)
df_forecast2 = pd.DataFrame({'Production dans '+ str(n) +" "+'jours' :forecast2},index=pd.date_range(start=datetime.date.today(),periods=period, freq='D'))
n_pro = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'),'production dans '+ str(n) +" "+'jours' :list(forecast2)})
df_forecast2.to_csv("Forecast2.csv")
forcast2=pd.read_csv('Forecast2.csv')
forcast2.rename(columns={"Unnamed: 0": "Date",'Production dans '+ str(n) +" "+'jours':"Production quantité tonne(s)"},inplace=True)
forcast2.head()
forcast2['Date'] = pd.to_datetime(forcast2['Date'],infer_datetime_format=True)
forcast2.index=forcast2['Date']
del forcast2['Date']
fig4 = pd.concat([data2,forcast2])

#pour le lstm

seq = 7 # nombre dobservations dans une séquence
n_fe = 1 # nombre de features

x = len(data) - 14

train = data.iloc[:x]
test = data.iloc[x:]
scaler.fit(train)
train_s = scaler.transform(train)
test_s = scaler.transform(test)

x2 = len(data2) - 14

train2 = data2.iloc[:x2]
test2 = data2.iloc[x2:]

scaler2 = MinMaxScaler()
scaler2.fit(train2)

train_s2 = scaler2.transform(train2)
test_s2 = scaler2.transform(test2)


def graph1():
    fig = plt.figure(figsize=(10,5))
    plt.plot(Pop3.prix_n, label="prix normalisé", color = 'darkviolet')
    plt.plot(Pop3.production_n, label="production normalisée", color = 'gold')
    plt.title("Représentation du prix au kilo et de la production")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig.savefig("static/images/Représentation du prix au kilo et de la production.png")

def graph2():
    fig2 = plt.figure(figsize=(10,5))
    plt.plot(data, label="prix au kilo", color = 'darkviolet') 
    plt.title("Représentation du prix au kilo au cours du temps")
    plt.xlabel("Année")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig2.savefig("static/images/Représentation du prix au kilo.png")

def graph3():
    fig3 = plt.figure(figsize=(10,5))
    plt.plot(data2, label="production", color = 'gold') 
    plt.title("Représentation de la production au cours du temps")
    plt.xlabel("Année")
    plt.ylabel("Production")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig3.savefig("static/images/Représentation de la production.png")


def predict_prix_ARIMA():
    nprix.savefig('static/images/Données prédites(Prix).png')
    return send_file('static/images/Données prédites(Prix).png')

def graph_prix_ARIMA1():
    fig12 = plt.figure(figsize=(10,5))
    plt.plot(forcast, label='prix dans '+ str(n) +" "+'jours', color = 'darkviolet')
    plt.title("Représentation du prix pour les données prédites")
    plt.xlabel("Jour")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig12.savefig("static/images/Représentation du prix (données prédites).png")
    return send_file("static/images/Représentation du prix (données prédites).png")

def graph_prix_ARIMA2():
    fig13 = plt.figure(figsize=(10,5))
    plt.plot(data, label="prix (valeurs observées)", color = 'darkviolet')
    plt.plot(forcast, label='prix dans '+ str(n) +" "+'jours', color = 'blue')
    plt.title("Représentation du prix avec les données prédites")
    plt.xlabel("Année")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig13.savefig("static/images/Représentation du prix (données prédites et données prédites).png")
    return send_file("static/images/Représentation du prix (données prédites et données prédites).png")
   
def predict_production_ARIMA():
    n_pro.savefig('static/images/Données prédites(Production).png')
    return send_file('static/images/Données prédites(Production).png')

def graph_pro_ARIMA1():
    fig14 = plt.figure(figsize=(10,5))
    plt.plot(forcast2, label='production dans '+ str(n) +" "+'jours', color = 'gold')
    plt.title("Représentation de la production pour les données prédites")
    plt.xlabel("Jour")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig14.savefig("static/images/Représentation de la production (données prédites).png")
    return send_file('static/images/Représentation de la production (données prédites).png')


def graph_pro_ARIMA2():
    fig15 = plt.figure(figsize=(10,5))
    plt.plot(data2, label="production (valeurs observées)", color = 'gold')
    plt.plot(forcast2, label='production dans '+ str(n) +" "+'jours', color = 'blue')
    plt.title("Représentation de la production avec les données prédites")
    plt.xlabel("Année")
    plt.ylabel("Production")
    plt.legend(loc="upper right")
    plt.grid(True)
    fig15.savefig("static/images/Représentation de la production (données historiques et données prédites).png")
    return send_file('static/images/Représentation de la production (données historiques et données prédites).png')


def graph_pred_prix_lstm():
    prediction_prix = []
    ca1 = train_s[-seq:]
    ca1 = ca1.reshape(1, seq, n_fe)
    future = period
    for i in range(len(test) + future):
        cp1 = mod3.predict(ca1)[0]
        prediction_prix.append(cp1)
        ca1 = np.append(ca1[:,1:,:],[[cp1]],axis=1)
    
    pred1 = scaler.inverse_transform(prediction_prix)
    ts1 = test.index
    for j in range(0, future):
        ts1 = ts1.append(ts1[-1:] + pd.DateOffset(1))
    
    Pred_prix = pd.DataFrame(columns = ['prix actuel', 'prix prédit'], index=pd.date_range(start=datetime.date.today(),periods=period, freq='D'))
    Pred_prix.loc[:,'prix prédit'] = pred1[:,0]
    Pred_prix.loc[:,'prix actuel'] = test["prix moyen au kg"]
    Ppi = Pred_prix['prix prédit'].tail(period)
    Ppi.savefig("static/images/Tableau des données prédites pour le prix(LSTM).png")
    Ppi2 = Ppi.plot(title = 'Prédiction du prix dans '+ str(n) +" "+' jours')
    Ppi2.savefig("static/images/Représentation graphique des données prédites pour le prix(LSTM).png")
    return send_file('static/images/Représentation graphique des données prédites pour le prix(LSTM).png')

def graph_pred_pro_lstm():
    prediction_pro = []
    ca2 = train_s2[-seq:]
    ca2 = ca2.reshape(1, seq, n_fe)
    future = period
    for i in range(len(test2) + future):
        cp2 = mod4.predict(ca2)[0]
        prediction_pro.append(cp2)
        ca2 = np.append(ca2[:,1:,:],[[cp2]],axis=1)
    
    pred2 = scaler.inverse_transform(prediction_pro)
    ts2 = test2.index
    
    for j in range(0, future):
        ts2 = ts2.append(ts2[-1:] + pd.DateOffset(1))

    Pred_pro = pd.DataFrame(columns = ['production actuelle', 'production prédite'], index = pd.date_range(start=datetime.date.today(),periods=period, freq='D'))
    Pred_pro.loc[:,'production prédite'] = pred2[:,0]
    Pred_pro.loc[:,'production actuelle'] = test2["Production quantité tonne(s)"]
    Po = Pred_pro['production prédite'].tail(period)
    Po.savefig("static/images/Tableau des données prédites pour la production(LSTM).png")
    Po2 = Po.plot(title = 'Prédiction du prix dans '+ str(n) +" "+' jours')
    Po2.savefig("static/images/Représentation graphique des données prédites pour le production(LSTM).png")
    return send_file('static/images/Représentation graphique des données prédites pour le production(LSTM).png')

"""
"""
@app.before_first_request
def create_all():
    db.create_all()
"""
#app.run(host='localhost', port=5000)

if __name__ == "__main__":
    app.run(debug=True)

<!--<div>Navigate: <a href="/index">Home</a>
          {% if current_user.is_anonymous %}
          <a href="{{ url_for('signup') }}">Sign up</a>
          {% else %}
          <a href="{{ url_for('signin') }}">Sign in</a>
          <a href="{{ url_for('logout') }}">Logout</a>
          {% endif %}
      </div>-->
      <!--<hr>
      {% block content %}{% endblock %}
      {% with messages = get_flashed_messages() %}
      {% if messages %}
      <ul>
          {% for message in messages %}
          <li>{{ message }}</li>
          {% endfor %}
      </ul>
      {% endif %}
      {% endwith %}
      -->

{% import 'bootstrap/wtf.html' as wtf %}
<p class="text-center">New user? <b><a href="{{ url_for('signup') }}">Signup</a></b></p>

{% block app_content %}
    
    <div class=container>
    	<div class="row">
    		<div class="col-md-4"></div>
        	<div class="col-md-4">
        		<h1 align="center">Sign Up</h1>
            	{{ wtf.quick_form(form) }}
            	<br>
           		<p align="center">Already have an account? <b><a href="{{ url_for('login') }}">Login</a></b></p>
       		</div>
       		<div class="col-md-4"></div>
    	</div>
	</div>
{% endblock %}

"""print("Choice of Number of days")
    day()

    print("Mongo DataBase")
    mg()

    print("Data loading")
    data()

    print("Data price and data production")
    d = ["Price","Production"]
    if d == "Price":
        data_prix
    else:
        data_pro

    print("Data Visualisation")
    g = ['Price and Production',"Price","Production"]
    if g == 'Price and Production':
        graph_u()

    elif g == "Price":
        graph_prix
    
    else:
        graph_pro

    print("Modelisation")
    M = ['ARIMA','LSTM']
    p = ['Price','Production']
    c = ['Table','Chart','All Chart']
    if M == 'ARIMA':
        if c == 'Table':
            if p == 'Price':
                predict_prix_ARIMA()
            else:
                predict_production_ARIMA()
        if c == 'Chart':
            if p == 'Price':
                graph_prix_ARIMA1()
            else:
                graph_pro_ARIMA1()

        if c == 'All Chart':
            if p == 'Price':
                graph_prix_ARIMA2()
            else:
                graph_pro_ARIMA2()
    if M == 'LSTM':
        if p == 'Price':
            graph_pred_prix_lstm()
        else:
            graph_pred_pro_lstm()"""

"""elif optradio11 == "on":
        g1 = arima.predict_prix_ARIMA()
    elif optradio12 == "on":
        g1 = arima.graph_prix_ARIMA1()
    elif optradio13 == "on":
        g1 = arima.graph_prix_ARIMA2()
    elif optradio14 == "on":
        g1 = arima.predict_production_ARIMA()
    elif optradio15 == "on":
        g1 = arima.graph_pro_ARIMA1()
    elif optradio16 == "on":
        g1 = arima.graph_pro_ARIMA2()
    elif optradio21 == "on":
        g1 = lstm.graph_pred_prix_lstm()
    elif optradio22 == "on":
        g1 = lstm.graph_pred_pro_lstm()"""

optradio11 = request.form.get('optradio11')
print(optradio11)
optradio12 = request.form.get('optradio12')
print(optradio12)
optradio13 = request.form.get('optradio13')
print(optradio13)
optradio14 = request.form.get('optradio14')
print(optradio14)
optradio15 = request.form.get('optradio15')
print(optradio15)
optradio16 = request.form.get('optradio16')
print(optradio16)
optradio21 = request.form.get('optradio21')
print(optradio21)
optradio22 = request.form.get('optradio22')
print(optradio22)


"""def day():
    n = input("Choose the number of days for predictions, between 1 and 30:")
    period = int(n)
    print(period)
    return period"""

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 

import pickle
from datetime import date
import time
timestr = time.strftime("%Y%m%d")
from keras.models import load_model




mod = pickle.load(open('modèle_ARIMA_Prix3.pkl', 'rb'))			
mod2 = pickle.load(open('modèle_ARIMA_Production3.pkl', 'rb'))
mod3 = load_model('prediction_prix_tomate_lstm_model_v1.h5')
mod4 = load_model('prediction_production_tomate_lstm_model_v1.h5')
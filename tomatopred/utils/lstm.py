from tomatopred.utils.MG import data_prix, data_pro, day, data
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from keras.models import load_model
from datetime import date
import time
timestr = time.strftime("%Y%m%d")
import pandas as pd
import numpy as np
import os
import dataframe_image as dfi

mod3 = load_model(r'tomatopred\models\prediction_prix_tomate_lstm_model_v1.h5')

mod4 = load_model(r'tomatopred\models\prediction_production_tomate_lstm_model_v1.h5')
chemin = os.path.join(os.getcwd(),'tomatopred','static','data','TMN.csv')
D1 = pd.read_csv(chemin, parse_dates=['Date'], dayfirst= True)
D1.sort_values(by=['Date'], inplace=True, ascending=True) 
D1 =  D1.set_index(['Date'])


def pred_prix_lstm(nbd):
    scaler = MinMaxScaler()
    seq = 7 # nombre dobservations dans une séquence
    n_fe = 1 # nombre de features pour le modèle
    lstm_prix = D1['prix moyen au kg']
    x = len(lstm_prix) * 0.7
    train = lstm_prix.iloc[:x]
    test = lstm_prix.iloc[x:]
    scaler.fit(train)
    train_s = scaler.transform(train)
    test_s = scaler.transform(test)

    prediction_prix = []
    ca1 = train_s[-seq:]
    ca1 = ca1.reshape(1, seq, n_fe)
    future = nbd
    for i in range(len(test) + future):
        cp1 = mod3.predict(ca1)[0]
        prediction_prix.append(cp1)
        ca1 = np.append(ca1[:,1:,:],[[cp1]],axis=1)
    
    pred1 = scaler.inverse_transform(prediction_prix)
    ts1 = test.index
    for j in range(0, future):
        ts1 = ts1.append(ts1[-1:] + pd.DateOffset(1))
    
    Pred_prix = pd.DataFrame(columns = ['prix actuel', 'prix prédit'], index=pd.date_range(start=date.today(),periods=future, freq='D'))
    Pred_prix.loc[:,'prix prédit'] = pred1[:,0]
    Pred_prix.loc[:,'prix actuel'] = test["prix moyen au kg"]
    Ppi = Pred_prix['prix prédit'].tail(future)
    return Ppi

def table_price_lstm(Ppi):
    chemin12 = os.path.join(os.getcwd(),'tomatopred','static','images','predicted_values(price)_table(LSTM).png')
    dfi.export(Ppi, chemin12)
    return ('predicted_values(price)_table(LSTM).png')

def graph_price_lstm(Ppi):
    Ppi2 = Ppi.plot(title = 'Prédiction du prix (valeurs prédites en fontion du nombre de jours choisis)')
    chemin10 = os.path.join(os.getcwd(),'tomatopred','static','images','predicted_values(price)_graph(LSTM).png')
    Ppi2.savefig(chemin10)
    return ('predicted_values(price)_graph(LSTM).png')

def pred_pro_lstm(nbd):
    scaler2 = MinMaxScaler()
    lstm_pro = D1['Production quantité tonne(s)']
    seq = 7 # nombre dobservations dans une séquence
    n_fe = 1 # nombre de features pour le modèle
    x2 = len(lstm_pro) * 0.7
    train2 = lstm_pro.iloc[:x2]
    test2 = lstm_pro.iloc[x2:]
    scaler2.fit(train2)
    train_s2 = scaler2.transform(train2)
    test_s2 = scaler2.transform(test2)

    prediction_pro = []
    ca2 = train_s2[-seq:]
    ca2 = ca2.reshape(1, seq, n_fe)
    future = nbd
    for i in range(len(test2) + future):
        cp2 = mod4.predict(ca2)[0]
        prediction_pro.append(cp2)
        ca2 = np.append(ca2[:,1:,:],[[cp2]],axis=1)
    
    pred2 = scaler.inverse_transform(prediction_pro)
    ts2 = test2.index
    
    for j in range(0, future):
        ts2 = ts2.append(ts2[-1:] + pd.DateOffset(1))

    Pred_pro = pd.DataFrame(columns = ['production actuelle', 'production prédite'], index = pd.date_range(start=date.today(),periods=future, freq='D'))
    Pred_pro.loc[:,'production prédite'] = pred2[:,0]
    Pred_pro.loc[:,'production actuelle'] = test2["Production quantité tonne(s)"]
    Po = Pred_pro['production prédite'].tail(future)
    return Po

def table_prod_lstm(Po):
    chemin13 = os.path.join(os.getcwd(),'tomatopred','static','images','predicted_values(production)_table(LSTM).png')
    dfi.export(Po, chemin13)
    return ('predicted_values(production)_table(LSTM).png')

def graph_prod_lstm(Po):
    Po2 = Po.plot(title = 'Prédiction de la prédiction (valeurs prédites en fontion du nombre de jours choisis)')
    chemin11 = os.path.join(os.getcwd(),'tomatopred','static','images','predicted_values(production)_graph(LSTM).png')
    Po2.savefig(chemin11)
    return ('predicted_values(production)_graph(LSTM).png')
    



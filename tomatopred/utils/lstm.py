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
import math
import datetime

mod3 = load_model('tomatopred/models/prediction_prix_tomate_lstm_model_v1.h5')

mod4 = load_model('tomatopred/models/prediction_production_tomate_lstm_model_v1.h5')
chemin = os.path.join(os.getcwd(),'tomatopred','static','data','TMN.csv')
D1 = pd.read_csv(chemin, parse_dates=['Date'], dayfirst= True)
D1.sort_values(by=['Date'], inplace=True, ascending=True) 
D1 =  D1.set_index(['Date'])

scaler = MinMaxScaler()
scaler2 = MinMaxScaler()
seq = 7 # nombre dobservations dans une séquence
n_fe = 1
n = 7
train_df = D1.sort_values(by=['Date']).copy()
date_index = train_df.index
FEATURES = ['Rafale max  help', 'soleil_durée',
       'Précipitations en mm', 'Température minimale en °C',
       'Température maximale en °C', 'prix moyen au kg',
       'Production quantité tonne(s)']

#pour le prix
def partition_dataset_price(seq, data11):
    x, y = [], []
    data_len = data11.shape[0]
    index_prix = data11.columns.get_loc("prix moyen au kg")
    for i in range(seq, data_len):
        x.append(data11[i-seq:i,:]) 
        y.append(data11[i, index_prix])
    
    
    x = np.array(x)
    y = np.array(y)
    return x, y

def pred_prix_lstm(nbd):
    data11 = pd.DataFrame(train_df)
    data_filtered = data11[FEATURES]
    data_filtered_ext = data_filtered.copy()
    data_filtered_ext['Prediction_Price'] = data_filtered_ext['prix moyen au kg']

    nrows = data_filtered.shape[0]
    np_data_unscaled = np.array(data_filtered)
    np_data = np.reshape(np_data_unscaled, (nrows, -1))
    scaler = MinMaxScaler()

    np_data_scaled = scaler.fit_transform(np_data_unscaled)
    scaler_pred = MinMaxScaler()
    df_Prix = pd.DataFrame(data_filtered_ext['prix moyen au kg'])
    np_Prix_scaled = scaler_pred.fit_transform(df_Prix)

    seq = 7 # nombre dobservations dans une séquence
    n_fe = 7 # nombre de features pour le modèle
    index_prix = data11.columns.get_loc("prix moyen au kg")
    train_data_len = math.ceil(np_data_scaled.shape[0] * 0.7)
    train_data = np_data_scaled[0:train_data_len, :]
    test_data = np_data_scaled[train_data_len - seq:, :]

    x_train, y_train = partition_dataset_price(seq, train_data)
    x_test, y_test = partition_dataset_price(seq, test_data)

    forecast_date = pd.date_range(date.today(), periods= nbd, freq = 'D').tolist()
    forecast = mod3.predict(x_train[-nbd:])
    fo_r = np.repeat(forecast,data11.shape[1], axis = -1)
    y_pred_fd = scaler_pred.inverse_transform(fo_r)[:,0]
    f_d = []
    for i in forecast_date:
        f_d.append(i.date())
    forecast3 = pd.DataFrame({'Date':np.array(f_d), 'Prix': y_pred_fd})
    forecast3 = forecast3.set_index(['Date'])

    return forecast3

def table_price_lstm(forecast3):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    prix_image = f'predicted_values_price_table_LSTM_{timestamp}.png'
    chemin7 = os.path.join(os.getcwd(),'tomatopred','static','images',prix_image)
    dfi.export(forecast3, chemin7)
    return prix_image

def graph_price_lstm(forecast3):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    prix_image2 = f'predicted_values_price_graph_LSTM_{timestamp}.png'
    Ppi2 = forecast3.plot(title = 'Prédiction du prix (valeurs prédites en fontion du nombre de jours choisis)')
    chemin10 = os.path.join(os.getcwd(),'tomatopred','static','images',prix_image2)
    Ppi2.savefig(chemin10)
    return prix_image2

#pour la production
def partition_dataset_pro(seq, data12):
    x, y = [], []
    data_len2 = data12.shape[0]
    index_pro = data12.columns.get_loc("Production quantité tonne(s)")
    for i in range(seq, data_len2):
        x.append(data12[i-seq:i,:]) 
        y.append(data12[i, index_pro])
    
    
    x = np.array(x)
    y = np.array(y)
    return x, y

def pred_pro_lstm(nbd):
    data12 = pd.DataFrame(train_df)
    data_filtered2 = data12[FEATURES]
    data_filtered_ext2 = data_filtered2.copy()
    data_filtered_ext2['Prediction_Production'] = data_filtered_ext2['Production quantité tonne(s)']

    nrows2 = data_filtered2.shape[0]
    np_data_unscaled2 = np.array(data_filtered2)
    np_data2 = np.reshape(np_data_unscaled2, (nrows2, -1))

    scaler2 = MinMaxScaler()
    np_data_scaled2 = scaler2.fit_transform(np_data_unscaled2)
    scaler_pred2 = MinMaxScaler()
    df_Pro = pd.DataFrame(data_filtered_ext2['Production quantité tonne(s)'])
    np_Pro_scaled = scaler_pred2.fit_transform(df_Pro)

    seq = 7 # nombre dobservations dans une séquence
    n_fe = 7 # nombre de features pour le modèle

    index_pro = data12.columns.get_loc("Production quantité tonne(s)")
    train_data_len2 = math.ceil(np_data_scaled2.shape[0] * 0.7)
    train_data2 = np_data_scaled2[0:train_data_len2, :]
    test_data2 = np_data_scaled2[train_data_len2 - seq:, :]

    x_train2, y_train2 = partition_dataset_pro(seq, train_data2)
    x_test2, y_test2 = partition_dataset_pro(seq, test_data2)

    forecast_date2 = pd.date_range(date.today(), periods= nbd, freq = 'D').tolist()
    forecasti2 = mod4.predict(x_train2[-nbd:])
    fo_r2 = np.repeat(forecasti2,data12.shape[1], axis = -1)
    y_pred_fd2 = scaler_pred2.inverse_transform(fo_r2)[:,0]
    f_d = []
    for i in forecast_date2:
        f_d.append(i.date())

    forecast4 = pd.DataFrame({'Date':np.array(f_d), 'Production': y_pred_fd2})
    forecast4 = forecast4.set_index(['Date'])

    return forecast4



def table_prod_lstm(forecast4):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pro_image = f'predicted_values_production_table_LSTM_{timestamp}.png'
    chemin7 = os.path.join(os.getcwd(),'tomatopred','static','images',pro_image)
    #df_forecast2.savefig(chemin7)
    dfi.export(forecast4, chemin7)
    return pro_image

def graph_prod_lstm(forecast4):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pro_image2 = f'predicted_values_production_graph_LSTM_{timestamp}.png'
    Po2 = forecast4.plot(title = 'Prédiction de la prédiction (valeurs prédites en fontion du nombre de jours choisis)')
    chemin11 = os.path.join(os.getcwd(),'tomatopred','static','images',pro_image2)
    Po2.savefig(chemin11)
    return pro_image2
    



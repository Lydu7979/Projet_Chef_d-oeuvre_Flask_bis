from utils.MG import data_prix, data_pro, day
import pickle
from datetime import date
import time
timestr = time.strftime("%Y%m%d")
import pandas as pd
import matplotlib.pyplot as plt
import os
import dataframe_image as dfi

mod = pickle.load(open(r'tomatopredict\models\modèle_ARIMA_Prix3.pkl', 'rb'))
			
mod2 = pickle.load(open(r'tomatopredict\models\modèle_ARIMA_Production3.pkl', 'rb'))

#prix
def prix_a(nbd):
    forecast,err,ci = mod.forecast(steps= nbd, alpha = 0.05)
    df_forecast = pd.DataFrame({'Prix dans '+  str(nbd) +" "+'jours' :forecast},index=pd.date_range(start=date.today(), periods=nbd, freq='D'))
    return df_forecast


#production
def pro_a(nbd):
    forecast2,err,ci = mod2.forecast(steps= nbd, alpha = 0.05)
    df_forecast2 = pd.DataFrame({'Production dans '+ str(nbd) +" "+'jours' :forecast2},index=pd.date_range(start=date.today(),periods=nbd, freq='D'))
    return df_forecast2


#Prédiction du prix

def predict_prix_ARIMA(df_forecast):
    chemin4 = os.path.join(os.getcwd(),'tomatopredict','static','images','predicted_values(price)_table(ARIMA).png')
    #df_forecast.savefig(chemin4)
    dfi.export(df_forecast, chemin4)
    return 'predicted_values(price)_table(ARIMA).png'

def graph_prix_ARIMA1(df_forecast):
    fig12 = plt.figure(figsize=(10,5))
    plt.plot(df_forecast, label="production (valeurs prédites)", color = 'darkviolet')
    plt.title("Représentation du prix pour les données prédites")
    plt.xlabel("Jour")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin5 = os.path.join(os.getcwd(),'tomatopredict','static','images','predicted_values(price)_graph(ARIMA).png')
    fig12.savefig(chemin5)
    return 'predicted_values(price)_graph(ARIMA).png'

def graph_prix_ARIMA2(df_forecast):
    fig13 = plt.figure(figsize=(10,5))
    plt.plot(data_prix(), label="prix (valeurs observées)", color = 'darkviolet')
    plt.plot(df_forecast, label="prix (valeurs prédites)", color = 'blue')
    plt.title("Représentation du prix avec les données prédites")
    plt.xlabel("Année")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin6 = os.path.join(os.getcwd(),'tomatopredict','static','images','all_values(price)_graph(ARIMA).png')
    fig13.savefig(chemin6)
    return 'all_values(price)_graph(ARIMA).png'
    

#Prédiction de la production

def predict_production_ARIMA(df_forecast2):
    chemin7 = os.path.join(os.getcwd(),'tomatopredict','static','images','predicted_values(production)_table(ARIMA).png')
    #df_forecast2.savefig(chemin7)
    dfi.export(df_forecast2, chemin7)
    return 'predicted_values(production)_table(ARIMA).png'

def graph_pro_ARIMA1(df_forecast2):
    fig14 = plt.figure(figsize=(10,5))
    plt.plot(df_forecast2, label="production (valeurs prédites)", color = 'gold')
    plt.title("Représentation de la production pour les données prédites")
    plt.xlabel("Jour")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin8 = os.path.join(os.getcwd(),'tomatopredict','static','images','predicted_values(production)_graph(ARIMA).png')
    fig14.savefig(chemin8)
    return 'predicted_values(production)_graph(ARIMA).png'

def graph_pro_ARIMA2(df_forecast2):
    fig15 = plt.figure(figsize=(10,5))
    plt.plot(data_pro(), label="production (valeurs observées)", color = 'gold')
    plt.plot(df_forecast2, label="production (valeurs prédites)", color = 'blue')
    plt.title("Représentation de la production avec les données prédites")
    plt.xlabel("Année")
    plt.ylabel("Production")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin9 = os.path.join(os.getcwd(),'tomatopredict','static','images','all_values(production)_graph(ARIMA).png')
    fig15.savefig(chemin9)
    return 'all_values(production)_graph(ARIMA).png'
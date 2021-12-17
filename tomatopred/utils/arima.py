from tomatopred.utils.MG import data_prix, data_pro
import pickle
from datetime import date, datetime
import time
timestr = time.strftime("%Y%m%d")
import pandas as pd
import matplotlib.pyplot as plt
import os
import dataframe_image as dfi


mod = pickle.load(open(r'tomatopred\models\modèle_ARIMA_Prix5.pkl', 'rb'))
			
mod2 = pickle.load(open(r'tomatopred\models\modèle_ARIMA_Production5.pkl', 'rb'))

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
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    prix_image = f'predicted_values_price_table_ARIMA_{timestamp}.png'
    chemin4 = os.path.join(os.getcwd(),'tomatopred','static','images',prix_image)
    #df_forecast.savefig(chemin4)
    dfi.export(df_forecast, chemin4)
    return prix_image

def graph_prix_ARIMA1(df_forecast):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    prix_image2 = f'predicted_values_price_graph_ARIMA_{timestamp}.png'
    fig12 = plt.figure(figsize=(10,5))
    plt.plot(df_forecast, label="prix (valeurs prédites)", color = 'darkviolet')
    plt.title("Représentation du prix pour les données prédites")
    plt.xlabel("Jour")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin5 = os.path.join(os.getcwd(),'tomatopred','static','images',prix_image2)
    fig12.savefig(chemin5)
    return prix_image2

def graph_prix_ARIMA2(df_forecast):
    fig13 = plt.figure(figsize=(10,5))
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    prix_image3 = f'all_values_price_graph_ARIMA_{timestamp}.png'
    plt.plot(data_prix(), label="prix (valeurs observées)", color = 'darkviolet')
    plt.plot(df_forecast, label="prix (valeurs prédites)", color = 'blue')
    plt.title("Représentation du prix avec les données prédites")
    plt.xlabel("Année")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin6 = os.path.join(os.getcwd(),'tomatopred','static','images',prix_image3)
    fig13.savefig(chemin6)
    return prix_image3
    

#Prédiction de la production

def predict_production_ARIMA(df_forecast2):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pro_image = f'predicted_values_production_table_ARIMA_{timestamp}.png'
    chemin7 = os.path.join(os.getcwd(),'tomatopred','static','images',pro_image)
    #df_forecast2.savefig(chemin7)
    dfi.export(df_forecast2, chemin7)
    return pro_image

def graph_pro_ARIMA1(df_forecast2):
    fig14 = plt.figure(figsize=(10,5))
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pro_image2 = f'predicted_values_production_graph_ARIMA_{timestamp}.png'
    plt.plot(df_forecast2, label="production (valeurs prédites)", color = 'gold')
    plt.title("Représentation de la production pour les données prédites")
    plt.xlabel("Jour")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin8 = os.path.join(os.getcwd(),'tomatopred','static','images',pro_image2)
    fig14.savefig(chemin8)
    return pro_image2

def graph_pro_ARIMA2(df_forecast2):
    fig15 = plt.figure(figsize=(10,5))
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pro_image3 = f'all_values_production_graph_ARIMA_{timestamp}.png'
    plt.plot(data_pro(), label="production (valeurs observées)", color = 'gold')
    plt.plot(df_forecast2, label="production (valeurs prédites)", color = 'blue')
    plt.title("Représentation de la production avec les données prédites")
    plt.xlabel("Année")
    plt.ylabel("Production")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin9 = os.path.join(os.getcwd(),'tomatopred','static','images',pro_image3)
    fig15.savefig(chemin9)
    return pro_image3
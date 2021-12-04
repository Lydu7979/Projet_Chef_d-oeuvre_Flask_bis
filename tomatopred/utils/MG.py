import sys
sys.path.insert(0, 'C:/Users/Simplon/OneDrive/Bureau/Formation/Projet_Chef_d-oeuvre_Flask_bis/')
import dns
import pymongo
import pandas as pd
import os

def get_client_mongodb(user_name = "Thmo89",psw = "Authentication "):
    
    uri2 = "mongodb+srv://{}:{}@cluster1.mknx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true".format(user_name, psw)

    client = pymongo.MongoClient(uri2)
    return client

def day():
    n = input("Choose the number of days for predictions, between 1 and 30:")
    period = int(n)
    print(period)
    return period

def mg():
    client = get_client_mongodb()
    db = client.Tomates_meteo_Centre8
    mycl = db["données"]
    Dat = pd.DataFrame(list(mycl.find()))
    Dat = Dat.drop(columns=["index"])
    return Dat

def data():
    chemin = os.path.join(os.getcwd(),'tomatopred','static','data','TMN.csv')
    print(chemin)
    i = mg()
    # DT = pd.DataFrame(i, columns = ['Date', 'prix moyen au kg', 'Production quantité \ntonne(s)', 'Température minimale en °C', 
    #                           'Température maximale en °C', 'précipitations en mm','Ensoleillement en min', 'Rafales (vitesse du vent) en km/h','catégorie tomates'])
    # DT.rename(columns={"Production quantité \ntonne(s)": "Production quantité tonne(s)"},inplace=True)
    # DT.to_csv(chemin,index = False)
    Pop = pd.read_csv(chemin, parse_dates=['Date'], dayfirst= True)
    Pop.sort_values(by=['Date'], inplace=True, ascending=True) 
    Pop =  Pop.set_index(['Date'])
    Pop2 = Pop.resample("D").mean()
    Pop2 = Pop2.interpolate()
    Pop3 = Pop2[['prix moyen au kg','Production quantité tonne(s)']]
    return Pop3 

def data_prix():
    d3 = data()
    d1 = d3['prix moyen au kg']
    return d1

def data_pro():
    d3 = data()
    d2 = d3['Production quantité tonne(s)']
    return d2
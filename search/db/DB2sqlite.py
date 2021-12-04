import sqlite3
import pandas as pd


def bdd_sql():
    conn = sqlite3.connect('data.db')
    dat3  = pd.read_sql_query("SELECT * FROM userstable", conn)
    dat3.reset_index(inplace=True)
    dat3 = dat3.rename(index = str, columns = {'index':'id_users'})
    dat3['Statut'] = 'utilisateur'
    dat3['Statut'][8] = 'administrateur'
    dummy_statut = pd.get_dummies(dat3['Statut']) # le code encode le statut du client.
    dat3 =  pd.merge(left=dat3,right=dummy_statut,left_index=True,right_index=True,)
    dat3 = dat3.drop(["Statut"], axis = 1)
    dat3.to_csv('Base_données/data_users.csv', index = False)
    dat4 = pd.read_csv('Base_données/data_users.csv') 
    
    conn.close()
    return dat4 









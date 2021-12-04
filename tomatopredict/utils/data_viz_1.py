from utils.MG import data, data_prix, data_pro
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os

D = data()
data1 = data_prix()
data2 = data_pro()
scaler = MinMaxScaler()


def graph_u():
    D[['prix_n', 'production_n']] = scaler.fit_transform(D[['prix moyen au kg', 'Production quantité tonne(s)']])
    fig = plt.figure(figsize=(10,5))
    plt.plot(D.prix_n, label="prix normalisé", color = 'darkviolet')
    plt.plot(D.production_n, label="production normalisée", color = 'gold')
    plt.title("Représentation du prix au kilo et de la production")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin = os.path.join(os.getcwd(),'tomatopredict','static','images','price_and_production.png')
    fig.savefig(chemin)
    return 'price_and_production.png'

def graph_prix():
    fig2 = plt.figure(figsize=(10,5))
    plt.plot(data1, label="prix au kilo", color = 'darkviolet') 
    plt.title("Représentation du prix au kilo au cours du temps")
    plt.xlabel("Année")
    plt.ylabel("Prix")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin2 = os.path.join(os.getcwd(),'tomatopredict','static','images','price.png')
    fig2.savefig(chemin2)
    return 'price.png'

def graph_pro():
    fig3 = plt.figure(figsize=(10,5))
    plt.plot(data2, label="production", color = 'gold') 
    plt.title("Représentation de la production au cours du temps")
    plt.xlabel("Année")
    plt.ylabel("Production")
    plt.legend(loc="upper right")
    plt.grid(True)
    chemin3 = os.path.join(os.getcwd(),'tomatopredict','static','images','production.png')
    fig3.savefig(chemin3)
    return 'production.png'
    

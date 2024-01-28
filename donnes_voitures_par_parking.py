import requests
import json
from datetime import datetime, timedelta
from urllib.parse import unquote


response = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
data = response.json()  # Convertit la réponse en données JSON

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)


def remplacer_caracteres(nom):
    mot_modifie = ""
    for caractere in nom:
        if caractere == ':':
            mot_modifie += '%3A'
        else:
            mot_modifie += caractere
    return mot_modifie

def ajouter_une_heure(date_str:str , nb:int):

    date_str = unquote(date_str)
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    nouvelle_date = date_obj + timedelta(hours=nb)
    nouvelle_date_str = nouvelle_date.strftime("%Y-%m-%dT%H:%M:%S")
    return nouvelle_date_str

Liste_nom=[]
Liste_id=[]
Liste2=[]

for i in data :
    id=i["id"]
    ch=id[len(id)-2:]
    if (ch!='20') and (ch!='21'):
        Liste_id.append(id)
        Liste2.append(i["totalSpotNumber"]["value"])

for i in data:
    nom=i["name"]["value"]
    Liste_nom.append(nom)

for i in range (len(Liste_id)):
    nom=Liste_id[i]
    id_link=remplacer_caracteres(nom)
    Liste_id[i]=id_link
print(Liste_id)
print(Liste2)

date_entree='2024-01-12'
heure_entree='00:00:00'
date_debut=(f'{date_entree}T{remplacer_caracteres(heure_entree)}')
print(date_debut)
date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))
print(date_fin)

jour=int(date_entree[8:10]) #Ca c'est la date du premier jour de la courbe 
for i in range(13,len(Liste_id)):
    for j in range(24):
        somme=0
        available=0

        reponse2 = requests.get(f"https://portail-api-data.montpellier3m.fr/parking_timeseries/{Liste_id[i]}/attrs/availableSpotNumber?fromDate={date_debut}&toDate={date_fin}")
        data2 = reponse2.json()  

        with open('data2.json', 'w') as file:
            json.dump(data2, file, indent=4)

        available+=data2["values"][0]
        somme += Liste2[i]
        pourcentage=round(((somme-available)/somme)*100,2)
        with open (f"taux_par_jour.txt",'a') as file:
            file.write(f"{str(Liste_nom[i])}:{str(pourcentage)}:{str(date_debut[11:13])}\n")
        somme=0
        available=0
        date_debut=remplacer_caracteres(ajouter_une_heure(date_debut,1))
        date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))
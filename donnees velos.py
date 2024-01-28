import requests
import json
from datetime import datetime, timedelta
from urllib.parse import unquote

response = requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
datav = response.json()  # Convertit la réponse en données JSON

with open('datav.json', 'w') as file:
    json.dump(datav, file, indent=4)


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


Liste_id=[]
Liste_nom=[]
Liste_total=[]



for i in range(len(Liste_id)):
    Liste_id[i]=remplacer_caracteres(Liste_id[i])


for i in datav:
    id=i["id"]
    ch=id[len(id)-2:]
    if (ch!='37') :
        Liste_nom.append(i["address"]["value"]["streetAddress"])
        Liste_id.append(i["id"])
        Liste_total.append(i["totalSlotNumber"]["value"])


for i in range(len(Liste_id)):
    Liste_id[i]=remplacer_caracteres(Liste_id[i])
#https://portail-api-data.montpellier3m.fr/bikestation_timeseries/urn%3Angsi-ld%3Astation%3A001/attrs/availableBikeNumber?fromDate=2023-12-20T00%3A00%3A00&toDate=2024-01-10T23%3A59%3A59


date_entree='2023-101-13'
heure_entree='00:00:00'
date_debut=(f'{date_entree}T{remplacer_caracteres(heure_entree)}')
print(date_debut)
date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))

jour=int(date_entree[8:10]) #Ca c'est la date du premier jour de la courbe 
def jour_mois(date):
    L_numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    L_mois = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'May', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
    for i in range(len(L_numeros)):
        if int(date) == L_numeros[i]:
            return L_mois[i]



for i in range(2):
    pourcentage_totale=0
    for i in range(24):
        somme=0
        available=0
        for j in range (len(Liste_id)):
            reponse2 = requests.get(f"https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{Liste_id[j]}/attrs/availableBikeNumber?fromDate={date_debut}&toDate={date_fin}")
            datav2 = reponse2.json()  

            with open('datav2.json', 'w') as file:
                json.dump(datav2, file, indent=4)
            available+=datav2["values"][0]
            somme += Liste_total[j]
            print(f"on a les donnes de {Liste_id[j]}")
        pourcentage=round(((somme-available)/somme)*100,2)
        with open ('semaine_janvier_velo.txt','a') as file:#Le nom du fichier ou seront stockées les informations des courbes se change a chaque fois
            file.write(f"{str(jour)} {jour_mois(date_entree[5:7])}:{date_debut[11:13]}:{pourcentage}\n")  #Le mois de récuperation des données aussi
        date_debut=remplacer_caracteres(ajouter_une_heure(date_debut,1))
        date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))
        pourcentage_totale+=pourcentage
    moyenne=(pourcentage_totale/24)
    jour+=1
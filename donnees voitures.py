import requests
import json
from datetime import datetime, timedelta
from urllib.parse import unquote

def ajouter_une_heure(date_str:str , nb:int):

    date_str = unquote(date_str)
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    nouvelle_date = date_obj + timedelta(hours=nb)
    nouvelle_date_str = nouvelle_date.strftime("%Y-%m-%dT%H:%M:%S")
    return nouvelle_date_str

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

Liste_id=[]
Liste2=[]
L_numeros=[1,2,3,4,5,6,7,8,9,10,11,12]
L_mois:['Janvier','Fevrier','Mars','Avril','May','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
def jour_mois(date):
    for i in range (len(L_numeros)):
        if (date==str(L_numeros[i])):
            return(L_mois[i])
    

Liste3=[]
for i in data :
    id=i["id"]
    ch=id[len(id)-2:]
    if (ch!='20') and (ch!='21') and (ch!='02'):
        Liste_id.append(id)
        Liste2.append(i["totalSpotNumber"]["value"])
        Liste3.append(i["name"]["value"])


print(Liste3)
for i in range (len(Liste_id)):
    nom=Liste_id[i]
    id_link=remplacer_caracteres(nom)
    Liste_id[i]=id_link
print(Liste_id)
print(Liste2)
'''''''''
def jour_mois(date):
    L_numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    L_mois = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'May', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
    for i in range(len(L_numeros)):
        if int(date) == L_numeros[i]:
            return L_mois[i]

#La date du debut de la courbe peut changer mais reste toujours sur cette forme
date_entree='2024-01-13'
heure_entree='00:00:00'
date_debut=(f'{date_entree}T{remplacer_caracteres(heure_entree)}')
print(date_debut)

date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))

jour=int(date_entree[8:10]) #Ca c'est la date du premier jour de la courbe 

for i in range(7):
    pourcentage_totale=0
    for i in range(24):
        somme=0
        available=0
        for j in range (len(Liste2)):
            reponse2 = requests.get(f"https://portail-api-data.montpellier3m.fr/parking_timeseries/{Liste_id[j]}/attrs/availableSpotNumber?fromDate={date_debut}&toDate={date_fin}")
            data2 = reponse2.json()  

            with open('data2.json', 'w') as file:
                json.dump(data2, file, indent=4)
            available+=data2["values"][0]
            somme += Liste2[j]
        pourcentage=round(((somme-available)/somme)*100,2)
        with open ('la nuit.txt','a') as file:#Le nom du fichier ou seront stockées les informations des courbes se change a chaque fois
            file.write(f"{str(jour)} {jour_mois(date_entree[5:7])}:{date_debut[11:13]}:{pourcentage}\n")  #Le mois de récuperation des données aussi
        date_debut=remplacer_caracteres(ajouter_une_heure(date_debut,1))
        date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))
        pourcentage_totale+=pourcentage
    moyenne=(pourcentage_totale/24)
    jour+=1




'''''''''














'''''''''
            somme=0
            available=0
            reponse2 = requests.get(f"https://portail-api-data.montpellier3m.fr/parking_timeseries/{Liste_id[j]}/attrs/availableSpotNumber?fromDate={date_debut}&toDate={date_fin}")
            data2 = reponse2.json()  # Convertit la réponse en données JSON

            with open('data2.json', 'w') as file:
                json.dump(data2, file, indent=4)

            available += data2["values"][0]
            somme += Liste2[j]
            available_totale += data2["values"][0]
            somme_totale += Liste2[j]
        pourcentage=round(((somme-available)/somme)*100,2)
        print(available)
        print(somme)
        print(pourcentage)

        pourcentage_totale=round((((somme_totale-available_totale)/somme_totale)*100),2)
        with open ('colors2.txt','a') as file:
            file.write(f"{a}Decembre:{date_debut[11:13]}:{pourcentage_totale}\n")
        date_debut=remplacer_caracteres(ajouter_une_heure(date_debut,1))
        date_fin=remplacer_caracteres(ajouter_une_heure(date_debut,1))
    a+=1

'''''''''
'''''''''
    date_debut = unquote(date_debut)
    date_obj = datetime.strptime(date_debut, '%Y-%m-%dT%H:%M:%S')
    date_debut = date_obj + timedelta(hours=1)
    print(date_debut)
    date_heure_obj = datetime.strptime(date_debut, '%Y-%m-%d %H:%M:%S')
    date_heure_formatee = date_heure_obj.strftime('%Y-%m-%dT%H:%M:%S')
    date_debut = quote(date_heure_formatee)

'''''''''

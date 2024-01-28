# Module de récupération de données via une API
# Copyright Dorian MILHAU
# Version 1.0
# Date: 08/01/24

import requests
import json
from datetime import datetime


class fonction_global:

    def __init__(self):
        pass

    def json(self,reponse):
        donnees = json.loads(reponse.text)
        with open("data.json", 'w') as fichier_json:
            json.dump(donnees, fichier_json, indent=2)
            fichier_json.close()
        self.fichier = json.load(open("data.json","r",encoding="UTF-8"))

    def diff_temps(self, temps1, temps2):
        liste = [temps1,temps2]
        for i in range(len(liste)):
            c = liste[i].replace('T',"-")
            c = c[:-1].replace(':',"-")
            c = c.replace(".","-")
            c = c.split("-")
            c = datetime(int(c[0]),int(c[1]),int(c[2]),int(c[3]),int(c[4]),int(c[5]),int(c[6]+'000'))
            liste[i] = c
        return abs(liste[0]-liste[1])



class Bikestation:

        def __init__(self, id=None, limite=1000) -> None:
            
            if id == None:
                response = requests.get(f"https://portail-api-data.montpellier3m.fr/bikestation?limit={limite}")
            else:
                response = requests.get(f"https://portail-api-data.montpellier3m.fr/bikestation?id=urn%3Angsi-ld%3Astation%3A{id}&limit={limite}")
            self.reponse = json.loads(response.text)

        def search_id_bikestation(self):
            response = requests.get(f"https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
            self.fichier = json.loads(response.text)
            id_list = []
            for i in self.fichier:
                id = i["id"][20:]
                if str(id) not in ['037']:
                    nom = i["address"]["value"]["streetAddress"]
                    total = i["totalSlotNumber"]["value"]
                    x = i["location"]["value"]["coordinates"][1]
                    y = i["location"]["value"]["coordinates"][0]
                    id_list.append([id,nom,total,(x,y)])
            return id_list
        
        def place(self):
            dispo = self.reponse["availableBikeNumber"]["value"]
            total = self.reponse["totalSlotNumber"]["value"]
            date = self.reponse["availableBikeNumber"]["metadata"]["timestamp"]["value"]
            return [dispo,total,date]

        def coordonnee_distance(self, obj=None):
            x = self.reponse["location"]["value"]["coordinates"][0]
            y = self.reponse["location"]["value"]["coordinates"][1]
            if obj != None:
                x1 = obj.reponse["location"]["value"]["coordinates"][0]
                y1 = obj.reponse["location"]["value"]["coordinates"][1]
                distance = ((x-x1)**2+(y-y1)**2)**0.5
                return [x,y,distance]
            return [x,y]
        
        def difference_temps(self, obj):
            date = self.reponse["availableBikeNumber"]["metadata"]["timestamp"]["value"]
            date1 = obj.reponse["availableBikeNumber"]["metadata"]["timestamp"]["value"]
            return fonction_global.diff_temps(date, date1)
        
        

class Historique_bikestation:

    def __init__(self, id, date_debut, date_fin) -> None:
        '''Format :
        id : 001
        Date : 2023-12-31T23:59:59'''
        #A traiter
        date_debut = date_debut.replace(":", "%3A")
        date_fin = date_fin.replace(":", "%3A")
        self.id = f"urn%3Angsi-ld%3Astation%3A{id}"
        response = requests.get(f"https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{self.id}/attrs/availableBikeNumber?fromDate={date_debut}&toDate={date_fin}")
        self.reponse = json.loads(response.text)
        
    def donnees(self):
        return [self.reponse["index"],self.reponse["values"]]
    
    def taux(self):
        print(self.reponse)
        places = self.reponse["values"]
        print(self.id)
        response = requests.get(f"https://portail-api-data.montpellier3m.fr/bikestation?id={self.id}&limit=1000")
        self.reponse = json.loads(response.text)
        
        print(self.reponse)
        self.total = self.reponse[0]["totalSlotNumber"]["value"]
        self.list_taux = []
        for place in places:
                self.list_taux.append(round((place/self.total)*100,2))
        return self.list_taux




class Offstreetparking:

        def __init__(self, id=None, limite=1000):
            self.id = id
            if id == None:
                response = requests.get(f"https://portail-api-data.montpellier3m.fr/offstreetparking?limit={limite}")
            else:
                id = f" urn%3Angsi-ld%3Aparking%3A{id}&"
                response = requests.get(f"https://portail-api-data.montpellier3m.fr/offstreetparking?{id}limit={limite}")
            self.reponse = json.loads(response.text)

        def search_id_parking(self):
            id_list = []
            for i in self.reponse:
                id = i["id"][20:]
                if str(id) not in ['020','021']:
                    total = i["totalSpotNumber"]["value"]
                    nom = i["name"]["value"]
                    x = i["location"]["value"]["coordinates"][1]
                    y = i["location"]["value"]["coordinates"][0]
                    id_list.append([id,nom,total,(x,y)])
            return id_list
        
        def place(self) -> list:
            place_liste = []
            for i in range(len(self.reponse)):
                dispo = self.reponse[i]["availableSpotNumber"]["value"]
                total = self.reponse[i]["totalSpotNumber"]["value"]
                date = self.reponse[i]["availableSpotNumber"]["metadata"]["timestamp"]["value"]
                place_liste.append([dispo,total,date])
            return place_liste

        def coordonnee_distance(self, obj=None):
            x = self.reponse[0]["location"]["value"]["coordinates"][0]
            y = self.reponse[0]["location"]["value"]["coordinates"][1]
            if obj != None:
                x1 = obj.reponse[0]["location"]["value"]["coordinates"][0]
                y1 = obj.reponse[0]["location"]["value"]["coordinates"][1]
                distance = ((x-x1)**2+(y-y1)**2)**0.5
                return [x,y,distance]
            return (x,y)     

        def difference_temps(self, obj):
            date = self.reponse[0]["availableSpotNumber"]["metadata"]["timestamp"]["value"]
            date1 = obj.reponse[0]["availableSpotNumber"]["metadata"]["timestamp"]["value"]
            return fonction_global.diff_temps(date, date1)

        def historique_parking(self, date_debut:str, date_fin:str):
            '''Format : 2023-12-31T23:59:59'''
            date_debut = date_debut.replace(":", "%3A")
            date_fin = date_fin.replace(":", "%3A")
            response = requests.get(f"https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A{self.id}/attrs/availableSpotNumber?fromDate={date_debut}&toDate={date_fin}")
            return json.loads(response.text)

        def places_pmr(self, offset, limite):
            response = requests.get(f"https://portail-api-data.montpellier3m.fr/pmr?id=urn%3Angsi-ld%3APmr%3A{self.id}&offset={offset}&limit={limite}")
            return json.loads(response.text)


class Historique_parking:

    def __init__(self, id, date_debut, date_fin) -> None:
        '''Format : 2023-12-31T23:59:59'''
        date_debut = date_debut.replace(":", "%3A")
        date_fin = date_fin.replace(":", "%3A")
        url = f"https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A{id}/attrs/availableSpotNumber?fromDate={date_debut}&toDate={date_fin}"
        print(url)
        response = requests.get(url)
        self.reponse = json.loads(response.text)
    
    def donnees(self):
        return [self.reponse["index"],self.reponse["values"]]


class Parking_spaces:
        
        def __init__(self, id:str, offset:int, limite:int) -> None:
            id = f"id=urn%3Angsi-ld%3AParkingSpace%3A{id}"
            response = requests.get(f"https://portail-api-data.montpellier3m.fr/parkingspaces?{id}&offset={offset}&limit={limite}")
            self.reponse = json.loads(response.text)

        def search_id_parking_spaces(self, space=False):
            response = requests.get(f"https://portail-api-data.montpellier3m.fr/parkingspaces?limit=1000")
            self.reponse = json.loads(response.text)
            id_list = []
            for i in self.reponse:
                id = i["id"][25:]
                nom = i["name"]
                nom = nom["value"]
                id_list.append([id,nom])
            return id_list

        def place(self):
            return ""



class Eco_compteur:

        def __init__(self, id:str, limite:int) -> None:
            response = requests.get(f"https://portail-api-data.montpellier3m.fr/ecocounter?id=urn%3Angsi-ld%3AEcoCounter%3A{id}&limit={limite}")
            self.reponse = json.loads(response.text)




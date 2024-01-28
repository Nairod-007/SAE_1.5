from api import Bikestation, Offstreetparking, Historique_parking, Historique_bikestation
from datetime import datetime
import json


def moyenne(points:list):
    return sum(points)/len(points)

def ecart_type(points:list,moyene:float):
    moyene = moyenne(points)
    somme = 0
    for i in range(len(points)):
        somme += (points[i]-moyene)**2
    return (somme/len(points))**0.5

def parking(date1:str,date2:str,voiture=True):
    if voiture:
        parkings = Offstreetparking().search_id_parking()
        print(parkings)
        for parking in parkings:
            donnees = parking_voiture_velo(parking[0],date1,date2,parking[2])
            gnuplot_launch(parking[0],parking[1],parking[2],donnees[0],donnees[1])
    else:
        parkings = Bikestation().search_id_bikestation()
        print(parkings)
        for parking in parkings:
            donnees = parking_voiture_velo(parking[0],date1,date2,parking[2],voiture=False)
            gnuplot_launch(parking[0],parking[1],parking[2],donnees[0],donnees[1],voiture=False)
        



def parking_voiture_velo(id:str,date_debut:str,date_fin:str,total:int,voiture=True):
    """ Format date : 2024-01-01T00:00:00 """
    print(id,date_debut,date_fin)
    if voiture:
        parking = Historique_parking(str(id),date_debut,date_fin)
        place = parking.donnees()
        chemin = f'parking/voiture/data/occupation_parking_voiture_{id}.txt'
    else:
        parking = Historique_bikestation(str(id),date_debut,date_fin)
        place = parking.donnees()
        print(place[0][-1][:-10])
        date1 = datetime.fromisoformat(place[0][-1])
        date2 = datetime.fromisoformat(date_fin+".000+00:00")
        difference = date2 - date1
        while difference.total_seconds() >= 300:
            date_debut = place[0][-1][:-10]
            parking1 = Historique_bikestation(str(id),date_debut,date_fin)
            liste = parking1.donnees()
            place[0].extend(liste[0])
            place[1].extend(liste[1])
            print(date2 - date1)
            date1 = datetime.fromisoformat(place[0][-1][:-10])
            date2 = datetime.fromisoformat(date_fin)
            difference = date2 - date1
        chemin = f'parking/velo/data/occupation_parking_velo_{id}.txt'


    data = ""
    for i in range(len(place[0])):
        date = place[0][i][:-10].replace("T", " ")
        place[1][i] = 100 - place[1][i]*100/total
        data+=f"{date} {place[1][i]}\n"

    with open(chemin, 'w') as gnuplot_file:
        gnuplot_file.write(data)
    return place


def gnuplot_launch(id,nom,total,dates,valeurs,voiture=True):
    moyenne_ = moyenne(valeurs)
    ecartype = ecart_type(valeurs, moyenne_)
    if voiture:
        vehicule = "voiture"
        parking = "parking"
        print(f"{dates[0][:19].replace('T',' ')}:{dates[-1]}")
    else:
        print("za")
        vehicule = "velo"
        parking = "parking"
        print(f"{dates[0][:10]}:{dates[-1]}")
    gnuplot_script = f"""
    set terminal png size 1920,1080 enhanced font 'arial,20'
    set output 'parking/{vehicule}/img/occupation_{parking}_{vehicule}_{id}.png'
    set title 'Graphique du parking : {nom} du {dates[0][:10]} au {dates[-1][:10]}'
    set key outside right center spacing 2
    set xlabel 'Temps'
    set ylabel 'Place'
    set yrange [0:105]
    
    condition(x) = (x > 80 ? x : 1/0)
    
    set xdata time
    set timefmt "%Y-%m-%d %H:%M:%S" # Format de temps pour les données (année-mois-jour heure:minute:seconde)
    set xtics format "%H:%M" time # Format des étiquettes de l'axe des abscisses (jour mois) ou %A (nom des différents jour)
    set xrange ["{dates[0][:19].replace("T"," ")}":"{dates[-1][:19].replace("T"," ")}"] # Plage de valeurs x
    #set xtics 250000 # Espacement des étiquettes de l'axe des abscisses (jour mois) uniquement activé quand je fais le calcul mois

    
    # Tracé de la courbe d'occupation du parking avec condition de coloration
    plot 100 with lines lc rgbcolor "#666666" title "Total de place : {total}",\
    'parking/{vehicule}/data/occupation_{parking}_{vehicule}_{id}.txt' using 1:(condition($3)) with filledcurves above y1=0 lc rgbcolor "#55BB0000" title "Occupation >= 80%",\
    '' using 1:3 with lines lc rgbcolor "#009900" title "Places occupées",\
    {moyenne_} with lines lc rgb 'red' title "Moyenne : {round(moyenne_,2)}",\
    {moyenne_+ecartype} with lines lc rgb 'blue' title "Ecart-Type : {round(ecartype,2)}",\
    {moyenne_-ecartype} with lines lc rgb 'blue' notitle

    """


    # Écrire le script Gnuplot dans un fichier
    with open('plot.gp', 'w') as gnuplot_file:
        gnuplot_file.write(gnuplot_script)

    # Appeler Gnuplot pour générer le graphique
    import subprocess
    subprocess.call(['gnuplot', 'plot.gp'])


parking("2023-11-22T00:00:00","2023-11-22T23:59:59",voiture=False)

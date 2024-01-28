from api import Offstreetparking,Bikestation
import folium


parkings = Offstreetparking().search_id_parking()
points_gps_voiture = []
for parking in parkings:
    points_gps_voiture.append([parking[3],parking[1]])
print(points_gps_voiture)

parkings = Bikestation().search_id_bikestation()
points_gps_velo = []
for parking in parkings:
    points_gps_velo.append([parking[3],parking[1]])
print(points_gps_velo)

couleurs = ['red', 'blue']

# Créer une carte centrée sur la première coordonnée GPS
carte = folium.Map(location=(43.59048, 3.884611), zoom_start=12,height="75%",width="75%")

# Ajouter des marqueurs pour chaque point GPS
for point in points_gps_voiture:
    folium.Marker(location=point[0],popup=point[1],icon=folium.Icon(color=couleurs[0]),tooltip="Parking voiture").add_to(carte)

for point in points_gps_velo:
    folium.Marker(location=point[0],popup=point[1],icon=folium.Icon(color=couleurs[1]),tooltip="Parking vélo").add_to(carte)

# Enregistrer la carte dans un fichier HTML
carte.save("carte.html")

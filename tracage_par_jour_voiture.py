#def tracage_courbe(nom_fichier:str , date_debut:str, date_fin:str):

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import defaultdict
import numpy as np
import math

with open('semaine_decembre_velo.txt', 'r') as file:
    lines = file.readlines()

data = {}
colors = plt.cm.get_cmap('tab20').colors

for line in lines:
    date, time_str, occupation = map(str.strip, line.split(':'))

    if date not in data:
        data[date] = {'times': [], 'occupations': []}

    data[date]['times'].append(float(time_str))
    data[date]['occupations'].append(float(occupation))

moyenne_general=0
for date, values in data.items():
    times = values['times']
    occupations = values['occupations']
    moyenne = round(np.mean(occupations),2)
    moyenne_general+=moyenne
moyenne_general=round(moyenne_general/7,2)
print(moyenne_general)
#plt.axhline(moyenne, linestyle='--', color=colors[len(plt.gca().lines) % len(colors)])



a=0
plt.figure(figsize=(12, 6))
for date, values in data.items():
    times = values['times']
    occupations = values['occupations']
    plt.plot(times, occupations, marker="o", linestyle='-', label=date, color=colors[len(plt.gca().lines) % len(colors)])
    moyenne = round(np.mean(occupations),2)
    a+=(moyenne-moyenne_general)**2
    print(f"Date: {date}, Moyenne: {moyenne}")
plt.axhline(moyenne_general, linestyle='--', color=colors[len(plt.gca().lines) % len(colors)])

plt.xlabel('Temps')
plt.ylabel('Occupation')
plt.title(f'Occupation Du 2023-12-16 -> 2023-12-22')

plt.legend(loc='upper left', bbox_to_anchor=(0.97, 1))

plt.grid(True)
plt.savefig("taux_occup_Decembre_velos.png")
plt.show()
a=a/7
a=a**0.5
print(a)




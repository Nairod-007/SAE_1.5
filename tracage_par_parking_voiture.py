
import matplotlib.pyplot as plt
import numpy as np

with open('taux_par_parking.txt', 'r') as file:
    lines = file.readlines()

data = {}
colors = plt.cm.get_cmap('tab20').colors

for line in lines:
    date, time_str, occupation = map(str.strip, line.split(':'))

    if date not in data:
        data[date] = {'times': [], 'occupations': []}

    data[date]['times'].append(float(time_str))
    data[date]['occupations'].append(float(occupation))

plt.figure(figsize=(15, 12))

for date, values in data.items():
    times = values['times']
    occupations = values['occupations']
    plt.plot(occupations, times, marker="o", linestyle='-', label=date, color=colors[len(plt.gca().lines) % len(colors)])
    moyenne = round(np.mean(occupations),2)
    #plt.axhline(moyenne, linestyle='--', color=colors[len(plt.gca().lines) % len(colors)])
    print(f"Date: {date}, Moyenne: {moyenne}")

plt.xlabel('Temps')
plt.ylabel('Occupation')
plt.title(f'Occupation Du 2024-01-19 00h --> 23h')

plt.legend(loc='upper left', bbox_to_anchor=(0.97, 1))


plt.grid(True)
plt.savefig("taz.png")
plt.show()





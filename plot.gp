
    set terminal png size 1920,1080 enhanced font 'arial,20'
    set output 'parking/velo/img/occupation_parking_velo_061.png'
    set title 'Graphique du parking : Jean de Beins du 2023-11-22 au 2023-11-22'
    set key outside right center spacing 2
    set xlabel 'Temps'
    set ylabel 'Place'
    set yrange [0:105]
    
    condition(x) = (x > 80 ? x : 1/0)
    
    set xdata time
    set timefmt "%Y-%m-%d %H:%M:%S" # Format de temps pour les donn�es (ann�e-mois-jour heure:minute:seconde)
    set xtics format "%H:%M" time # Format des �tiquettes de l'axe des abscisses (jour mois) ou %A (nom des diff�rents jour)
    set xrange ["2023-11-22 00:00:07":"2023-11-22 23:59:05"] # Plage de valeurs x
    #set xtics 250000 # Espacement des �tiquettes de l'axe des abscisses (jour mois) uniquement activ� quand je fais le calcul mois

    
    # Trac� de la courbe d'occupation du parking avec condition de coloration
    plot 100 with lines lc rgbcolor "#666666" title "Total de place : 16",    'parking/velo/data/occupation_parking_velo_061.txt' using 1:(condition($3)) with filledcurves above y1=0 lc rgbcolor "#55BB0000" title "Occupation >= 80%",    '' using 1:3 with lines lc rgbcolor "#009900" title "Places occup�es",    73.80642361111111 with lines lc rgb 'red' title "Moyenne : 73.81",    76.76410876094597 with lines lc rgb 'blue' title "Ecart-Type : 2.96",    70.84873846127626 with lines lc rgb 'blue' notitle

    
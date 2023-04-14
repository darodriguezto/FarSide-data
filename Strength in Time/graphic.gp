set title 'Strength by day'
set grid
set ylabel 'Strength'
set xlabel 'Date'
set xdata time
set xtics offset -2.7,graph -0.1 rotate by 30
set timefmt "%Y.%m.%d.%h"
plot 'datos.txt' u 1:2 ps 0.5 pt 1 t 'Total strength by day'
set term pdf
set out '2022.pdf'
replot
exit
set title 'ETA at east limb'
set grid
set ylabel 'Strength'
set xlabel 'Date'
set xdata time
set xtics offset -2.7,graph -0.1 rotate by 29
set timefmt "%Y-%m-%d"
plot 'ETAlist.txt' u 2:1 w p t ''
set term pdf
set out 'ETAgraphic.pdf'
replot
exit
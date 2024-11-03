
	
# Requires data files "[123].dat" from this directory,
# so change current working directory to this directory before running.
# gnuplot> set term <term-type>
# gnuplot> load 'simple.dem'
#
set title "Obráběcí rychlost v závislosti na průměru" font ",20"
set yrange [95:3890]
set grid
set logscale x
set xtics 1.13
set ytics 100
#set tics font "Helvetica,8"
set format x "%.1f cm"
set ylabel "rychlost otáčení (min^{-1})"
set xlabel "průměr obrobku (cm)"
set terminal pdfcairo size 29.7cm,21cm

g(d)=10/(pi*x/100)*60
f(d)=15/(pi*x/100)*60

xmax=53.3
set xrange [4.5:xmax]

plot '+' using 1:(f($1)):(g($1)) with filledcurves fs transparent solid 0.30 lc rgb "blue"  title "vhodná rychlost obrábění (10 ms^{-1} až 15 ms^{-1})"



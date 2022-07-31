set terminal qt

set title "{currency} Exchange Rate"

set timefmt "%Y-%m-%d"

set xdata time
set xrange [ "{start_date:%Y-%m-%d}":"{end_date:%Y-%m-%d}" ]
set xlabel "Date"

set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5
plot '{data_file}' using 1:2 title "" with linespoints ls 1

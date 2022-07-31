set terminal dumb

set title "{currency} Exchange Rate"

set timefmt "%Y-%m-%d"

set xdata time
set xrange [ "{start_date:%Y-%m-%d}":"{end_date:%Y-%m-%d}" ]
set xlabel "Date"

plot '{data_file}' using 1:2 title "" with linespoints pt "x"

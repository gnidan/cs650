set term pdf enhanced
set output 'fp_ops_min_norm.pdf'
set data style linespoints
set key below
set title 'FFT PAPI Total Floating Point Operations (Minimum) (Normalized)'
set xlabel 'FFT Size (log_2)'
set xtic 2
set ylabel 'Operations'
plot \
'../data/kd_fftr2_norm.dat' using 2:10 title 'fftr2' with linespoints , \
'../data/kd_fftr2_opt_norm.dat' using 2:10 title 'fftr2\_opt' with linespoints , \
'../data/fft_four1_norm.dat' using 2:10 title 'four1' with linespoints , \
'../data/DFT_rec_norm.dat' using 2:10 title 'DFT\_rec' with linespoints , \
'../data/DFT_buf_rec_norm.dat' using 2:10 title 'DFT\_buf\_rec' with linespoints, \
'../data/fftw_estimate_norm.dat' using 2:10 title 'fftw\_estimate' with linespoints, \
'../data/fftw_measure_norm.dat' using 2:10 title 'fftw\_measure' with linespoints

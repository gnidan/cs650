set term pdf enhanced
set output 'l1dcm_ave_norm.pdf'
set data style linespoints
set key below
set title 'FFT PAPI L1 Data Cache Misses (Average) (Normalized)'
set xlabel 'FFT Size (log_2)'
set xtic 2
set ylabel 'Misses'
plot \
'../data/kd_fftr2_norm.dat' using 2:12 title 'fftr2' with linespoints , \
'../data/kd_fftr2_opt_norm.dat' using 2:12 title 'fftr2\_opt' with linespoints , \
'../data/fft_four1_norm.dat' using 2:12 title 'four1' with linespoints , \
'../data/DFT_rec_norm.dat' using 2:12 title 'DFT\_rec' with linespoints , \
'../data/DFT_buf_rec_norm.dat' using 2:12 title 'DFT\_buf\_rec' with linespoints, \
'../data/fftw_estimate_norm.dat' using 2:12 title 'fftw\_estimate' with linespoints, \
'../data/fftw_measure_norm.dat' using 2:12 title 'fftw\_measure' with linespoints

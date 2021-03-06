set term pdf enhanced
set output 'l1dcm_min.pdf'
set data style linespoints
set key below
set title 'FFT PAPI L1 Data Cache Misses (Minimum)'
set xlabel 'FFT Size (log_2)'
set xtic 2
set ylabel 'Misses (log_{10})'
set logscale y
plot \
'../data/kd_fftr2.dat' using 2:13 title 'fftr2' with linespoints , \
'../data/kd_fftr2_opt.dat' using 2:13 title 'fftr2\_opt' with linespoints , \
'../data/fft_four1.dat' using 2:13 title 'four1' with linespoints , \
'../data/DFT_rec.dat' using 2:13 title 'DFT\_rec' with linespoints , \
'../data/DFT_buf_rec.dat' using 2:13 title 'DFT\_buf\_rec' with linespoints, \
'../data/fftw_estimate.dat' using 2:13 title 'fftw\_estimate' with linespoints, \
'../data/fftw_measure.dat' using 2:13 title 'fftw\_measure' with linespoints

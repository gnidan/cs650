# Calibrator v0.9e
# (by Stefan.Manegold@cwi.nl, http://www.cwi.nl/~manegold/)
 set term pdf enhanced
 set output 'calibrator-out.cache-replace-time.pdf'
#set term gif transparent interlace small size 500, 707 # xFFFFFF x333333 x333333 x0055FF x005522 x660000 xFF0000 x00FF00 x0000FF
#set output 'calibrator-out.cache-replace-time.gif'
set data style linespoints
set key below
set title 'calibrator-out.cache-replace-time'
set xlabel 'memory range [bytes]'
set x2label ''
set ylabel 'nanosecs per iteration'
set y2label 'cycles per iteration'
set logscale x 2
set logscale x2 2
set logscale y 10
set logscale y2 10
set format x '%1.0f'
set format x2 '%1.0f'
set format y '%1.0f'
set format y2 ''
set xrange[0.750000:163840.000000]
#set x2range[0.750000:163840.000000]
set yrange[1.000000:1000.000000]
#set y2range[1.000000:1000.000000]
set grid x2tics
set xtics mirror ('1k' 1, '' 2, '4k' 4, '' 8, '16k' 16, '' 32, '64k' 64, '' 128, '256k' 256, '' 512, '1M' 1024, '' 2048, '4M' 4096, '' 8192, '16M' 16384, '' 32768, '64M' 65536, '' 131072)
set x2tics mirror ('[32k]' 32, '[4M]' 4096)
set y2tics ('(3)' 4.140000, '(8)' 10.250000, '(92)' 114.910000, '0.8' 1, '8' 10, '80' 100, '800' 1000)
set label 1 '(3.75)  ' at 0.750000,3.750000 right
set arrow 1 from 0.750000,3.750000 to 163840.000000,3.750000 nohead lt 0
set label 2 '(10)  ' at 0.750000,10.000000 right
set arrow 2 from 0.750000,10.000000 to 163840.000000,10.000000 nohead lt 0
set label 3 '(115)  ' at 0.750000,115.000000 right
set arrow 3 from 0.750000,115.000000 to 163840.000000,115.000000 nohead lt 0
 set label 4 '^{ Calibrator v0.9e (Stefan.Manegold\@cwi.nl, www.cwi.nl/~manegold) }' at graph 0.5,graph 0.02 center
#set label 4    'Calibrator v0.9e (Stefan.Manegold@cwi.nl, www.cwi.nl/~manegold)'    at graph 0.5,graph 0.03 center
plot \
0.1 title 'stride:' with points pt 0 ps 0 , \
'calibrator-out.cache-replace-time.data' using 1:($7-0.000000) title '256' with linespoints lt 1 pt 3 , \
'calibrator-out.cache-replace-time.data' using 1:($13-0.000000) title '\{128\}' with linespoints lt 2 pt 4 , \
'calibrator-out.cache-replace-time.data' using 1:($19-0.000000) title '\{64\}' with linespoints lt 3 pt 5 , \
'calibrator-out.cache-replace-time.data' using 1:($25-0.000000) title '32' with linespoints lt 4 pt 6 , \
'calibrator-out.cache-replace-time.data' using 1:($31-0.000000) title '16' with linespoints lt 5 pt 7 , \
'calibrator-out.cache-replace-time.data' using 1:($37-0.000000) title '8' with linespoints lt 6 pt 8
set nolabel
set noarrow

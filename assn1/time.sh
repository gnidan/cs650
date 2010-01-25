#!/bin/sh

ITERATIONS=10

export LD_LIBRARY_PATH=/site/local/papi_x86_64/lib:${HOME}/local/fftw-2.1.5-kodiak
for fft in 4 5 6 7; do
    n=1
    while [ $n -lt 25 ]; do
        ./src/time_fft $n $ITERATIONS $fft $test
        $n+=1
    done
done

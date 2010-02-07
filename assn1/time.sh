#!/bin/sh

ITERATIONS=10
TEST=0

export LD_LIBRARY_PATH=/site/local/papi_x86_64/lib:${HOME}/local/fftw-2.1.5-kodiak

START=$1
STOP=$2
STEP=$3
shift 3

for fft; do
    n=$START
    while [ $n -lt $STOP ]; do
			  ./src/time_fft $n $ITERATIONS $fft $TEST 
        n=$(( $n + $STEP))
    done
done

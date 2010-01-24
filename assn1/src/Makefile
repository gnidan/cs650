.PHONY: all

CC := gcc
CFLAGS := -g -Wall --pedantic --std=c99
LDFLAGS := -lm

ifdef FFTW
CFLAGS += -DFFTW -I$(HOME)/local/include
LDFLAGS += -L$(HOME)/local/lib -lfftw
endif

PROGS := time_fft

all: $(PROGS)

time_fft: time_fft.o fft.o test.o four1.o
	$(CC) -o $@ $^ $(LDFLAGS)

clean:
	@$(RM) -f *.o *~ $(PROGS)

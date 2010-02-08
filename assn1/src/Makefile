.PHONY: all

CC := gcc
<<<<<<< HEAD
CFLAGS := -g -Wall --pedantic --std=c99
LDFLAGS := -lm
=======
CFLAGS := -Wall --pedantic --std=c99
LDFLAGS := -lm

ifdef OPT
CFLAGS += -O3 -march=nocona
else
CFLAGS += -g
endif

ifdef FFTW
FFTW_DIR := $(HOME)/local/fftw-2.1.5-kodiak
CFLAGS += -DFFTW -I$(FFTW_DIR)/include
LDFLAGS += -L$(FFTW_DIR)/lib -lfftw
endif

ifdef PAPI
PAPI_DIR := /site/local/papi_x86_64
CFLAGS += -DPAPI -I$(PAPI_DIR)/include
LDFLAGS += -L$(PAPI_DIR)/lib -lpapi
endif
>>>>>>> c5eddd98fbc801fe9c169601d90298712dcf2831

PROGS := time_fft

all: $(PROGS)

<<<<<<< HEAD
time_fft: time_fft.o fft.o test.o four1.o
	$(CC) $(LDFLAGS) -o $@ $^
=======
time_fft: time_fft.o fft.o test.o four1.o fft4.o
	$(CC) -o $@ $^ $(LDFLAGS)
>>>>>>> c5eddd98fbc801fe9c169601d90298712dcf2831

clean:
	@$(RM) -f *.o *~ $(PROGS)

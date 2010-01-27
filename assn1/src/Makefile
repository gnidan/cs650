.PHONY: all

CC := gcc
CFLAGS := -g -Wall --pedantic --std=c99
LDFLAGS := -lm

ifdef OPT
CFLAGS += -O3 -march=nocona
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

PROGS := time_fft

all: $(PROGS)

time_fft: time_fft.o fft.o test.o four1.o fft4.o
	$(CC) -o $@ $^ $(LDFLAGS)

clean:
	@$(RM) -f *.o *~ $(PROGS)

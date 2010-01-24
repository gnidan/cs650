.PHONY: all

CC := gcc
CFLAGS := -g -Wall --pedantic --std=c99
LDFLAGS := -lm

ifdef FFTW
CFLAGS += -DFFTW -I$(HOME)/local/include
LDFLAGS += -L$(HOME)/local/lib -lfftw
endif

ifdef PAPI
PAPI_DIR := /site/local/papi_x86_64
CFLAGS += -DPAPI -I$(PAPI_DIR)/include
LDFLAGS += -L$(PAPI_DIR)/lib -lpapi
endif

PROGS := time_fft

all: $(PROGS)

time_fft: time_fft.o fft.o test.o four1.o
	$(CC) -o $@ $^ $(LDFLAGS)

clean:
	@$(RM) -f *.o *~ $(PROGS)

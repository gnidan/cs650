.PHONY: all

CC := gcc
CFLAGS := -g -Wall --pedantic --std=c99
LDFLAGS := -lm

PROGS := time_fft

all: $(PROGS)

time_fft: time_fft.o fft.o test.o four1.o
	$(CC) $(LDFLAGS) -o $@ $^

clean:
	@$(RM) -f *.o *~ $(PROGS)

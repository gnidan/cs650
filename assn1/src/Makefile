.PHONY: all

CC := gcc
CFLAGS := -Wall --pedantic --std=c99
LDFLAGS :=

PROGS := numrec_time

all: $(PROGS)

numrec_time: main.o four1.o
	$(CC) -o $(LDFLAGS) $@ $^

clean:
	@$(RM) -f *.o *~ $(PROGS)

# Trivial makefile to build samples generator, to run it with example and to analyze
# the results

# how many samples to generate
COUNT := 30000
# which distribution to use
DISTR := example/fio-random-loop_0-oio_8-rw_70-bs_4096.dist_table

TMPFILE := $(shell mktemp)


all: le check clean
	@echo Done

le: le.c
	$(CC) -o le -g le.c

check: le
	./le $(DISTR) $(COUNT) > $(TMPFILE)
	@echo TBF checking the distribution


clean:
	echo rm -f le $(TMPFILE)
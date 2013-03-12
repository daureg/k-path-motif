rm=/bin/rm -f
VALGRIND=valgrind --tool=memcheck --track-origins=yes
CC?=cc
DEFS=
INCLUDES=
LIBS=
ZCOV_DIR=zcov
BIN_DIR=bin

DEFINES=$(INCLUDES) $(DEFS)
DEBUG=1
WARNINGS=-Wall -Wextra -pedantic
COMMON=-std=c99 $(DEFINES) $(WARNINGS)
DEBUG_FLAG=-O0 -g -fprofile-arcs -ftest-coverage -D__DEBUG_
RELEASE_FLAGS=-march=native -mtune=native -O3 -fomit-frame-pointer -funroll-loops
CFLAGS=$(COMMON)
ifeq ($(DEBUG), 1)
	CFLAGS+=$(DEBUG_FLAG)
else
	CFLAGS+=$(RELEASE_FLAGS)
endif

all: find_k_motif

x: all
	$(BIN_DIR)/find_k_motif

x-valgrind: all
	$(VALGRIND) $(BIN_DIR)/find_k_motif

find_k_motif: find_k_motif.o gf2q.o reader.o
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/find_k_motif find_k_motif.c reader.o gf2q.o $(LIBS)

reader.o: reader.c
	$(CC) $(CFLAGS) -c reader.c $(LIBS)

find_k_motif.o: find_k_motif.c
	$(CC) $(CFLAGS) -c find_k_motif.c $(LIBS)

gf2q.o: gf2q.c
	$(CC) $(CFLAGS) -c gf2q.c $(LIBS)

# Need check framework: http://check.sourceforge.net/
check_k_motif.o: check_k_motif.c
	$(CC) $(CFLAGS) -c check_k_motif.c

check_k_motif: check_k_motif.o reader.o gf2q.o
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) -o $(BIN_DIR)/check_k_motif check_k_motif.o reader.o gf2q.o $(shell pkg-config --libs check)

check: check_k_motif
	$(BIN_DIR)/check_k_motif

# Need zcov script: https://github.com/ddunbar/zcov
cov: check
	LANG=C $(ZCOV_DIR)/zcov-scan out.zcov .
	LANG=C $(ZCOV_DIR)/zcov-genhtml out.zcov covreport

cov-clean:
	rm -rf covreport/
	$(rm) out.zcov
	find -name "*.gc*" -delete

# Need valgrind tool: http://valgrind.org/
valgrind: check_k_motif
	CK_FORK=no $(VALGRIND) $(BIN_DIR)/check_k_motif

clean: cov-clean
	$(rm) *.o core *~
	rm -rf $(BIN_DIR)

astyle:
	astyle -r -n "*.c" "*.h"

dist: check clean
	git archive --prefix=336978_Lefalher/ -o 336978_Lefalher.zip HEAD

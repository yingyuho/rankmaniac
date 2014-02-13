CXX = gcc
CFLAGS = -O3

all: rmap rreduce rawcat preduce

rmap: rank_map.c
	$(CXX) rank_map.c -o rmap $(CFLAGS)

rreduce: rank_reduce.c
	$(CXX) rank_reduce.c -o rreduce $(CFLAGS)

rawcat: raw_cat.c
	$(CXX) raw_cat.c -o rawcat $(CFLAGS)

preduce: heap.c heap.h process_reduce.c
	$(CXX) process_reduce.c heap.c -o preduce $(CFLAGS)

clean:
	rm -f rmap rreduce rawcat preduce *.out

.PHONY: all clean

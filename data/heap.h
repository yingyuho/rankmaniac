#ifndef __HEAP_H__
#define __HEAP_H__

/* Maximum number of values that can be stored in the heap. */
#define MAX_HEAP_ELEMS 50

/*
 * A simple heap data structure, for storing floats.
 */
typedef struct
{
  int node_id;
  float cpr;
  float ppr;
} pageRank;
 
typedef struct
{
  /* Number of values currently in the heap. */
  int num_values;

  /* The values in the heap. */
  pageRank values[MAX_HEAP_ELEMS];
} float_heap;

void copy_PR(pageRank *src, pageRank *dst);

/* Initialize a heap data structure. */
void init_heap(float_heap *pHeap);

/* Returns the first (i.e. smallest) value in the heap. */
void get_first_value(float_heap *pHeap, pageRank *buf);

/* Adds another value to the heap, in the proper place. */
void add_value(float_heap *pHeap, pageRank * newval);

#endif /* __HEAP_H__ */


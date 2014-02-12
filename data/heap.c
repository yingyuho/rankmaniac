#include <assert.h>
#include <stdlib.h>
#include "heap.h"


/*
 * These are declarations of local functions that are used
 * internally by the heap data structure, but are not visible
 * outside this module.
 */

void sift_down(float_heap *pHeap, int index);
void sift_up(float_heap *pHeap, int index);
void swap_values(float_heap *pHeap, int i, int j);

/*
 * For heaps stored in an array, left child and right child
 * of a particular index are calculated using these functions.
 * The "index" value is supposed to be an integer.
 */
#define  LEFT_CHILD(index) (2 * (index) + 1)
#define RIGHT_CHILD(index) (2 * (index) + 2)

/* Given an index, the parent index is computed as follows.
 * The "index" value is supposed to be an integer.
 */
#define PARENT(index) (((index) - 1) / 2)


/* Initialize a heap data structure. */
void init_heap(float_heap *pHeap)
{
  assert(pHeap != NULL);
  pHeap->num_values = 0;
}

void copy_PR(pageRank * src, pageRank * dst)
{
  dst->node_id = src->node_id;
  dst->cpr = src->cpr;
  dst->ppr = src->cpr;
}


/* Returns the first (i.e. smallest) value in the heap. */
void get_first_value(float_heap *pHeap, pageRank * buf)
{
  assert(buf != NULL);
  assert(pHeap != NULL);

  /* There needs to be at least one value left in the heap! */
  assert(pHeap->num_values > 0);

  /* Smallest value is at the root - index 0. */
  copy_PR(&(pHeap->values[0]), buf);

  /* Decrease the count of how many values are in the heap.
   * NOTE that if there was more than one value in the heap,
   * the last value is still at values[num_values], so we have
   * to move it to the new vacancy that opened up at the root.
   * If there was only one value in the heap when "get-first"
   * was called, we're done.
   */
  pHeap->num_values--;
  if (pHeap->num_values)
  {
    /* Move the last value in the heap to the root. */
    copy_PR(&(pHeap->values[pHeap->num_values]), &(pHeap->values[0]));

    /* Sift down the new value to position it properly
     * in the heap.
     */
    sift_down(pHeap, 0);
  }

  return result;
}


/* Adds another value to the heap, in the proper place. */
void add_value(float_heap *pHeap, pageRank * newval)
{
  int index;

  assert(pHeap != NULL);
  assert(pHeap->num_values >= 0);

  /* There needs to be room for one more element in the heap... */
  assert(pHeap->num_values < MAX_HEAP_ELEMS);

  /* Add the new value to the end of the heap, then sift up. */

  index = pHeap->num_values;
  copy_PR(&(pHeap->values[index]), buf);
  pHeap->num_values++;

  /* If the new value isn't at the root, sift up. */
  if (index != 0)
    sift_up(pHeap, index);
}



/*==================*/
/* HELPER FUNCTIONS */
/*==================*/


/*
 * Given a heap and an index, sift_down checks to see if the value
 * at that index needs to be "sifted downward" in the heap, to
 * preserve the heap properties.  Specifically, a value needs to
 * be moved down in the heap if it is greater than either of its
 * children's values.  (This is the "order" property.)  In order
 * to preserve the "shape" property of heaps, the value is swapped
 * with the *smaller* of its two child values.
 *
 * If a value only has a left child, then only the left child is
 * examined for the swap.
 *
 * If a value has both left and right children, it is possible
 * that one child may be larger than the value, while the other is
 * smaller than the value.  Since we swap with the smallest child
 * value, we preserve the heap properties even in that situation.
 */
void sift_down(float_heap *pHeap, int index)
{
  assert(pHeap != NULL);
  assert(index < pHeap->num_values);

  int left_child = LEFT_CHILD(index);
  int right_child = RIGHT_CHILD(index);

  if (left_child >= pHeap->num_values)
  {
    /* If the left child's index is past the end of the heap
     * then this value has no children.  We're done.
     */
    return;
  }

  if (right_child >= pHeap->num_values)
  {
    /* Only have a left child. */

    if ((&(pHeap->values[left_child]))->cpr < (&(pHeap->values[index]))->cpr)
    {
      /* Left child value is smaller.  Swap this value and the
       * left child value.
       */
      swap_values(pHeap, index, left_child);

      /* Don't need to call sift_down again, because if this
       * node only has a left child, we are at the bottom of
       * the heap.
       */
    }
  }
  else
  {
    /* This value has a left and right child. */

    float left_val = (&(pHeap->values[left_child]))->cpr;
    float right_val = (&(pHeap->values[right_child]))->cpr;
    int swap_child;

    if (left_val < (&(pHeap->values[index]))->cpr ||
        right_val < (&(pHeap->values[index]))->cpr)
    {
      /* Need to swap this node with one of its children.  Pick
       * the smaller of the two children, since this is a min-heap
       * and that will preserve the heap properties.
       */
      if (left_val < right_val)
        swap_child = left_child;
      else
        swap_child = right_child;

      /* Do the swap, then call sift_down again, in case we aren't
       * at the bottom of the heap yet.
       */
      swap_values(pHeap, index, swap_child);
      sift_down(pHeap, swap_child);
    }
  }
}


/*
 * Given a heap and an index, sift_up checks to see if the value
 * at that index needs to be "sifted upward" in the heap, to
 * preserve the heap properties.  Specifically, a value needs to
 * be moved up in the heap if it is less than its parent value.
 * (This is just the "order" property; the "shape" property is
 * not affected by sifting a value up.)
 */
void sift_up(float_heap *pHeap, int index)
{
  int parent_index = PARENT(index);

  /* If the index to sift up is the root, we are done. */
  if (index == 0)
    return;

  assert(parent_index >= 0);
  assert(parent_index != index);  /* Parent of index 0 = 0... that's bad. */

  /* If the specified value is smaller than its parent value then
   * we have to swap the value and its parent.
   */
  if ((&(pHeap->values[index]))->cpr < (&(pHeap->values[parent_index]))->cpr)
  {
    /* Swap the value with its parent value. */
    swap_values(pHeap, index, parent_index);

    /* If we haven't gotten to the root, we might have to
     * sift up again.
     */
    if (parent_index != 0)
      sift_up(pHeap, parent_index);
  }
}


/*
 * Helper function to handle the onerous task of swapping two
 * values in the value array of a heap.
 */
void swap_values(float_heap *pHeap, int i, int j)
{
  pageRank tmp;

  assert(pHeap != NULL);
  assert(i >= 0 && i < pHeap->num_values);
  assert(j >= 0 && j < pHeap->num_values);
  assert(i != j);

  copyPR(&(pHeap->values[i]), &tmp);
  copyPR(&(pHeap->values[j]), &(pHeap->values[i]));
  copyPR(&tmp, &(pHeap->values[j]));
}


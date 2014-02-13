#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "heap.h"

#define RLINE 100
#define BUFSIZE 4096
#define TOPNUM 30
#define EPSILON 2E-3f

int main(void) {
    setvbuf(stdout, NULL, _IOFBF, BUFSIZE);
    setvbuf(stdin,  NULL, _IOFBF, BUFSIZE);

    size_t all_id_cap = 131072;
    size_t all_id_len = 0;
    int * all_id = (int*) malloc(all_id_cap * sizeof(int*));
    
    char * line = NULL;
    size_t len = 0;
    ssize_t line_len;
    char key[32];
    char * id = NULL;
    int node_id;

    ssize_t key_len;
    char * value = NULL;

    char * start = NULL;
    char * end = NULL;
    int final = 0;
    int toStop = 1;

    int deg;
    float cpr, ppr;
    int i;
    float toppages[TOPNUM];
    pageRank toppr[TOPNUM];
    
    float_heap prHeap;
    pageRank pr;
    pageRank * curr_toppage;
    
    init_heap(&prHeap);
    
    while ((line_len = getline(&line, &len, stdin)) != -1) {
        line[--line_len] = '\0';
        value = strchr(line, '\t');
        if (value) {
            key_len = value++ - line;
            strncpy(key, line, key_len);
            key[key_len] = '\0';
            
            node_id = strtol(key, &end, 10);
            if (!memcmp(value, "F", 1)) {
                end = value + 2;
                final = 1;
                if (*end)
                    cpr = strtof(end, &end);
                (&pr)->node_id = node_id;
                (&pr)->cpr = cpr;
                (&pr)->ppr = 0;
                add_value(&prHeap, &pr);
            }
            else {
                deg = strtol(value, &end, 10); ++end;
                cpr = strtof(end, &end); ++end;
                ppr = strtof(end, &end); ++end;
                
                (&pr)->node_id = node_id;
                (&pr)->cpr = cpr;
                (&pr)->ppr = ppr;

                // store all node id for cancelling profiles during final round
                all_id[all_id_len++] = node_id;
                if (all_id_len == all_id_cap) {
                    all_id_cap *= 2;
                    all_id = (int*) realloc(all_id, all_id_cap * sizeof(int*));
                }
                
                if ((&prHeap)->num_values < TOPNUM) {
                    add_value(&prHeap, &pr);
                }
                else if ((&((&prHeap)->values[0]))->cpr < cpr) {
                    get_first_value(&prHeap, NULL);
                    add_value(&prHeap, &pr);
                }
            }
            if (!final) {
                printf("N:%d\t%s\n", node_id, value);
            }
        }
    }
    if (line)
        free(line);
        
    curr_toppage = (&prHeap)->values;
    for (i = 0; i < TOPNUM; i++) {
        cpr = curr_toppage->cpr;
        ppr = curr_toppage->ppr;
        if ((cpr - ppr) / ppr > EPSILON || (cpr - ppr) / ppr < -EPSILON)
            toStop = 0;
        curr_toppage++;
    }

    if (toStop || final) {
        i = 29;
        while ((&prHeap)->num_values) {
            get_first_value(&prHeap, &(toppr[i]));
            i--;
        }
        for (i = 0; i < 20; i++)
            printf("FinalRank:%f\t%d\n", (&(toppr[i]))->cpr, (&(toppr[i]))->node_id);

        if (!final)
            for (i = 0; i < all_id_len; i++)
                printf("FinalRank:\t%d\n", all_id[i]);
    }
    return 0;
}

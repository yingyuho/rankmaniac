#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "heap.h"

#define RLINE 100
#define BUFSIZE 2048
#define TOPNUM 30
#define EPSILON 2E-3f

int main(void) {
    
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
                if (*end)
                    cpr = strtof(end, &end);
                printf("FinalRank:%f\t%d\n", cpr, node_id);
            }
            else {
                deg = strtol(value, &end, 10); ++end;
                cpr = strtof(end, &end); ++end;
                ppr = strtof(end, &end); ++end;
                
                (&pr)->node_id = node_id;
                (&pr)->cpr = cpr;
                (&pr)->ppr = ppr;
                
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
    if (toStop) {
        while ((&prHeap)->num_values) {
            get_first_value(&prHeap, &pr);
            printf("FinalRank:%f\t%d\n", (&pr)->cpr, (&pr)->node_id);
        }
    }
    return 0;
}

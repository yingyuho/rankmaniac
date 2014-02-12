#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define A       0.85f

#define BUFSIZE 4096

#define KEYSIZE 16

// two line buffers that will be used alternately
static char * lines[2] = {NULL, NULL};
static int line_to_use = 0;
static char * curr_line;
static char * profile = NULL;


static size_t len = 0;
static ssize_t line_len;

static char keys[2*KEYSIZE];
static char * curr_key;
static char * prev_key;

static char * id;

static char * curr_value;
// static char * prev_value;

static char * field;
static char * end;

static float prc = 0.f;
static float prn = 0.f;

static int finalized = 0;
static int hasProfile = 0;



// TODO: something based on prev_line, prev_key, prev_value when key changes or EOF
void end_of_key(void) {
/*
 * # Python equivalent
 *
 * if not final:
 *     if profile != None:
 *         prn += prc
 *         if len(profile) == 4:
 *             sys.stdout.write('%s\t%s,%s,%s,%s\n' % (node_id, profile[0], prn, profile[1], profile[3]))
 *         else:
 *            sys.stdout.write('%s\t%s,%s,%s\n' % (node_id, profile[0], prn, profile[1]))
 */
    // printf("key: %s => %s\n", prev_key, curr_key);

    if (!finalized && hasProfile) {
        // updated PR
        // prc += prn * A;

        end = profile;

        // Skip attr[0] = "P"
        field = strsep(&end, ",");
        // if ((field = strsep(&end, ",")) == NULL) return;

        // Get attr[1] = degree and print the first piece
        field = strsep(&end, ",");

        printf("%s\t%s,%f", prev_key, field, prc + prn * A);

        // Get and print attr[2] = current PR
        field = strsep(&end, ",");
        printf(",%s", field);

        // Skip attr[3] = previous PR
        field = strsep(&end, ",");

        // Print the edges, if any
        if (end != NULL) 
            printf(",%s\n", end);
        else
            printf("\n");

    }

    hasProfile = 0;
    prc = prn = 0.f;
}

void swap_ptr(size_t * a, size_t * b) {
    *a ^= *b; *b ^= *a; *a ^= *b;
}


int main(void) {
    curr_line = lines[line_to_use];
    curr_key = keys;
    prev_key = keys + KEYSIZE;

    while ((line_len = getline(&curr_line, &len, stdin)) != -1) {
        // rstrip
        curr_line[--line_len] = '\0';
        curr_value = strchr(curr_line, '\t');

        // strsep() will replace '\t' by '\0' and point value
        // to the character following '\t'
        if (curr_value) {
            *curr_value = '\0';
            strcpy(curr_key, curr_line);
            *curr_value++ = '\t';

            // printf("key: %s => %s\n", prev_key, curr_key);

            if (strcmp(curr_key, prev_key))
                end_of_key();

            // TODO: Something based on curr_line, curr_key, curr_value

            end = curr_value;

            if (!memcmp(curr_value, "F", 1)) {
                finalized = 1;

                if (strchr(curr_value, ',') != NULL)
                    printf("%s\n", curr_line);

            } else if (!finalized) {
                if (!memcmp(curr_value, "P", 1)) {
                    hasProfile = 1;
                    profile = curr_value;

                    // Skip attr[0] = "P" and attr[1] = degree
                    field = strsep(&end, ",");
                    field = strsep(&end, ",");
                    *(--field) = ',';

                    // Parse attr[2] = current PR
                    field = strsep(&end, ",");
                    prc = strtof(field, NULL);
                    *(--field) = ',';

                    if (*end != '\0')
                        *(end-1) = ',';

                    // if ((field = strsep(&end, ",")) != NULL) {
                    //     prc = strtof(field, NULL);
                    //     *(--field) = ',';
                    // }
                } else {
                    // Parse attr[0] = PR to add to NodeID = key
                    prn += strtof(curr_value, NULL);
                    // printf("prn = %f\n", prn);
                }
            }
            // End TODO

            // Swap key buffers
            swap_ptr((size_t*) &curr_key, (size_t*) &prev_key);

            curr_line = lines[line_to_use ^= 1];
        }
    }

    if (hasProfile)
        end_of_key();

    if (lines[0])
        free(lines[0]);
    if (lines[1])
        free(lines[1]);

    return 0;
}
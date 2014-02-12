#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define A       0.85f
#define SLINE   1E-4f
#define DLINE   0.8f

#define BUFSIZE 4096

int count_fields(const char * str, char sep) {
    int n = (*str != '\0');

    while ((str = strchr(str, sep)) != NULL) {
        ++n;
        ++str;
    }

    return n;
}

int main(void) {
    char * line = NULL;

    size_t len = 0;
    ssize_t line_len;

    char * key;
    char * id;

    char * value;
    char * field;

    // setvbuf(stdout, NULL, _IOFBF, BUFSIZE);
    // setvbuf(stdin,  NULL, _IOFBF, BUFSIZE);

    while ((line_len = getline(&line, &len, stdin)) != -1) {
        // rstrip
        line[--line_len] = '\0';
        value = strchr(line, '\t');

        // strsep() will replace '\t' by '\0' and point value
        // to the character following '\t'
        if (value) {
            *value++ = '\0';
            key = line;

            if (!memcmp(key, "NodeId:", 2)) {
                id = key + 7;

                int deg = count_fields(value, ',') - 2;

                // Get attr[0] and convert to float
                field = strsep(&value, ",");
                float rankToGive = strtof(field, NULL);

                // printf("%s\tP,%d,%f,%s\n", id, deg, 0.0, value);
                // printf("%s\t%f\n", id, (1. - A) / A);
                printf("%s\tP,%d,%f,%s\n", id, deg, 1.0, value);
                printf("%s\t%f\n", id, -1.0);

                // Skip attr[1]
                strsep(&value, ",");

                if (deg) {
                    rankToGive /= (float) deg;
                    // Process attr[i], i >= 2
                    while ((field = strsep(&value, ",")) != NULL)
                        printf("%s\t%f\n", field, rankToGive);
                        // printf("%s\t%f,%s\n", field, rankToGive, id);
                } else {
                    printf("%s\t%f\n", id, rankToGive);
                }

            } else if (!memcmp(key, "N:", 2)) {
                id = key + 2;

                // Parse attr[0]
                int deg = strtol(value, &field, 10); ++field;

                // Parse attr[1]
                float cpr = strtof(field, &field); ++field;

                // Parse attr[2]
                float ppr = strtof(field, &field); ++field;

                float rankToGive = cpr - ppr;

                int dead = 0;

                if (deg == 0) {
                    printf("%s\t%f\n", id, rankToGive);
                } else {
                    rankToGive /= deg;
                    if (cpr < DLINE && (rankToGive < SLINE && rankToGive > -SLINE)) {
                        dead = 1;
                    } else if (*(field - 1) != '\0') {
                        // attr[i], i > 2
                        char * end = field;
                        while ((field = strsep(&end, ",")) != NULL) {
                            printf("%s\t%f\n", field, rankToGive);
                            // put ',' back to '\0' created by strsep()
                            // so value is a single string again
                            *(--field) = ',';
                        }
                    }
                }

                if (!dead)
                    printf("%s\tP,%s\n", id, value);

            } else if (!memcmp(key, "FinalRank:", 1)) {
                char * rank = key + 10;
                if (!strcmp(rank, ""))
                    printf("%s\tF\n", value);
                else
                    printf("%s\tF,%s\n", value, rank);
            }
        }
    }

    if (line)
        free(line);

    return 0;
}
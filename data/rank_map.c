#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define A       0.85f
#define SLINE   1E-5f
#define DLINE   0.8f

#define BUFSIZE 2048

int count_fields(const char * str, char sep) {
    const char * start = str;
    const char * end;

    int n = (*str != '\0');

    while ((end = strchr(start, sep)) != NULL) {
        ++n;
        start = end + 1;
    }

    return n;
}

int main(void) {
    // char outBuf[BUFSIZE];
    // char inBuf[BUFSIZE];

    char * line = NULL;
    size_t len = 0;
    ssize_t line_len;
    char key[32];
    char * id = NULL;

    ssize_t key_len;
    char * value = NULL;

    char * start = NULL;
    char * end = NULL;

    int num_fields = 0;

    setvbuf(stdout, NULL, _IOFBF, BUFSIZE);
    setvbuf(stdin,  NULL, _IOFBF, BUFSIZE);

    while ((line_len = getline(&line, &len, stdin)) != -1) {
        line[--line_len] = '\0';
        value = strchr(line, '\t');
        if (value) {
            key_len = value++ - line;
            strncpy(key, line, key_len);
            key[key_len] = '\0';

            if (!memcmp(key, "NodeId:", 2)) {
                id = key + 7;

                int deg = count_fields(value, ',') - 2;

                printf("%s\tP,%d,%s,%s\n", id, deg, "0.0", value + 4);

                printf("%s\t%f,%s\n", id, (1. - A) / A, id);

                float rankToGive = strtof(value, &end);

                char * end;

                rankToGive = strtof(value, &end);

                if (deg) {
                    rankToGive /= (float) deg;

                    for (end = strchr(end + 1, ',') + 1; *end; ++end) {
                        if (*end != ',')
                            putchar(*end);
                        else
                            printf("\t%f,%s\n", rankToGive, id);
                    }
                    printf("\t%f,%s\n", rankToGive, id);

                } else {
                    rankToGive = strtof(value, &end);
                    printf("%s\t%f,%s\n", id, rankToGive, id);
                }

            } else if (!memcmp(key, "N:", 2)) {
                id = key + 2;

                // for (char* end = line; *end; end++)
                //     printf("%d ", (int)*end);
                // printf("\n");
                // for (char* end = id; *end; end++)
                //     printf("%d ", (int)*end);
                // printf("\n");
                // printf("line = %s\n", line);
                // printf("id = %s;\n", id);
                // printf("val = %s;\n", value);

                char * end;

                // attr[0]
                int deg = strtol(value, &end, 10); ++end;
                // printf("%s\n", end);
                // attr[1]
                float cpr = strtof(end, &end); ++end;
                // attr[2]
                float ppr = strtof(end, &end); ++end;
                float rankToGive = cpr - ppr;

                int dead = 0;

                if (deg == 0) {
                    printf("%s\t%f,%s\n", id, rankToGive, id);
                } else if (*end) {
                    rankToGive /= deg;
                    if (cpr < DLINE && (rankToGive < SLINE && rankToGive > -SLINE)) {
                        dead = 1;
                        printf("%s\tD\n", id);
                    } else {
                        // attr[n], n>2
                        for (; *end; ++end) {
                            if (*end != ',')
                                putchar(*end);
                            else {
                                printf("\t%f,%s\n", rankToGive, id);
                // printf("line = %s\n", line);
                // printf("id = %s;\n", id);
                // printf("val = %s;\n", value);
                            }
                        }
                        printf("\t%f,%s\n", rankToGive, id);
                // printf("line = %s\n", line);
                // printf("id = %s;\n", id);
                // printf("val = %s;\n", value);
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
/*-
 * Copyright (c) 1989, 1993
 *  The Regents of the University of California.  All rights reserved.
 *
 * This code is derived from software contributed to Berkeley by
 * Kevin Fall.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 4. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/*-
 * This source code is derived from 
 * http://www.opensource.apple.com/source/text_cmds/text_cmds-71/cat/cat.c
 */


#include <sys/param.h>
#include <sys/stat.h>

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <err.h>

const char *filename = "stdin";

int main (void)
{
    int rfd = fileno(stdin);
    int off, wfd;
    ssize_t nr, nw;
    static size_t bsize;
    static char *buf = NULL;
    struct stat sbuf;

    wfd = fileno(stdout);
    if (buf == NULL) {
        if (fstat(wfd, &sbuf))
            err(1, "%s", filename);
        bsize = MAX(sbuf.st_blksize, 1024);
        if ((buf = malloc(bsize)) == NULL)
            err(1, "buffer");
    }
    while ((nr = read(rfd, buf, bsize)) > 0)
        for (off = 0; nr; nr -= nw, off += nw)
            if ((nw = write(wfd, buf + off, (size_t)nr)) < 0)
                err(1, "stdout");
    if (nr < 0) {
        warn("%s", filename);
        exit(1);
    }
    exit(0);
}
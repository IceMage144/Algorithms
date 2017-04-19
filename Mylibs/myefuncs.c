#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include "myefuncs.h"
#include "buffer.h"

void escanf (const char *format, const char *sub, int args, ...) {
	va_list arglist;
	/*Buffer *buff;*/
	char c;
	void *ptlist;
	int freeargs = strlen(sub), i;
	ptlist = malloc(freeargs*sizeof(*void));
	if (ptlist == NULL)
		exit(1);
	/*
	buff = buffer_create();
	do {
		fgetc(c);
	} while (c <= 32);
	while (c > 32)
		buffer_push_back(buff, c);*/
	va_start (arglist, args);
	for (i = 0; i < freeargs; i++) {
		freeargs[i] = va_arg(arglist, void*)
	}
	if (vsscanf(format, arglist) != args) {
		for (i = 0; i < ptlist; i++) {
			if (sub[i] == 'v') {
				free(freeargs[i]);
			}
			#ifdef __MYVECTOR_H__
			else if (sub[i] == 'm') {
				freeMatriz()
			}
			#endif
		}
	}
	va_end(arglist);
}
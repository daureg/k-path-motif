#include <stdio.h>
#include <stdlib.h>
#include "reader.h"

int main() {
	int n, m, c, k;
	graph_t* g=NULL;
	int* color_freq=NULL;
	skipws(stdin);

	while (!feof(stdin)) {

		graph_read(&g, &color_freq, &n, &m, &k, &c);
		/* Print out what we just read in. */
		fprintf(stdout,
		        "parameters: n = %d, m = %d, c = %d, k = %d\n",
		        n, m, c, k);
		graph_print(g, color_freq, c);

		/* Release memory & consider next graph. */
		FREE(color_freq);
		graph_free(g);
		skipws(stdin);
	}

	return EXIT_SUCCESS;
}

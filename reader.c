#include "reader.h"

/* 4 helper subroutines. */
static void error(const char* fn, int line, const char* func,
                  const char* format, ...) {
	va_list args;
	va_start(args, format);
	fprintf(stderr,
	        "ERROR [file = %s, line = %d]\n"
	        "%s: ",
	        fn,
	        line,
	        func);
	vfprintf(stderr, format, args);
	fprintf(stderr, "\n");
	va_end(args);
	abort();
}

static void* malloc_wrapper(size_t size) {
	void* p = malloc(size);

	if (p == NULL) {
		ERROR("malloc fails");
	}

	return p;
}

void free_wrapper(void* p) {
	free(p);
}
/* Skip whitespace and comments. */
void skipws(FILE* in) {
	int c;

	do {
		c = fgetc(in);

		if (c == '#') {
			do {
				c = fgetc(in);
			}
			while (c != EOF && c != '\n');
		}
	}
	while (c != EOF && isspace(c));

	if (c != EOF) {
		ungetc(c, in);
	}
}

static int* enlarge(int m, int m_was, int* was) {
	assert(m >= 0 && m_was >= 0);
	int* a = (int*) MALLOC(sizeof(int)*m);
	int i;

	if (was != (void*) 0) {
		for (i = 0; i < m_was; i++) {
			a[i] = was[i];
		}

		FREE(was);
	}

	return a;
}

void graph_alloc(graph_t** g, int n) {
	assert(n >= 0);
	int i;
	*g = (graph_t*) MALLOC(sizeof(graph_t));
	(*g)->num_vertices = n;
	(*g)->num_edges = 0;
	(*g)->edge_capacity = 100;
	(*g)->edges = enlarge(2*(*g)->edge_capacity, 0, (void*) 0);
	(*g)->colors = (int*) MALLOC(sizeof(int)*n);

	for (i = 0; i < n; i++) {
		(*g)->colors[i] = 0;
	}
}

void graph_free(graph_t* g) {
	FREE(g->edges);
	FREE(g->colors);
	FREE(g);
}

void graph_add_edge(graph_t* g, int u, int v) {
	assert(u >= 0 &&
	       v >= 0 &&
	       u != v &&
	       u < g->num_vertices &&
	       v < g->num_vertices);

	if (g->num_edges == g->edge_capacity) {
		g->edges = enlarge(4*g->edge_capacity, 2*g->edge_capacity, g->edges);
		g->edge_capacity *= 2;
	}

	assert(g->num_edges < g->edge_capacity);
	int* e = g->edges + 2*g->num_edges;
	g->num_edges++;
	e[0] = u;
	e[1] = v;
}

void graph_set_color(graph_t* g, int u, int c) {
	assert(u >= 0 && u < g->num_vertices && c >= 0);
	g->colors[u] = c;
}

void graph_print(graph_t* g, int* color_freq, int num_colors) {
	int i;
	for (i = 0; i < g->num_edges; i++)
		fprintf(stdout,
				"%s{%d,%d}",
				i == 0 ? "edge list: " : " ",
				g->edges[2*i+0] + 1,
				g->edges[2*i+1] + 1);

	fprintf(stdout, "\ncoloring [vertex (color)]:");

	for (i = 0; i < g->num_vertices; i++) {
		fprintf(stdout, " %d(%d)", i, g->colors[i]);
	}

	fprintf(stdout, "\nmotif [color (frequency)]:");

	for (i = 0; i < num_colors; i++) {
		fprintf(stdout, " %d(%d)", i, color_freq[i]);
	}

	fprintf(stdout, "\n");
	fflush(stdout);
}

void graph_read(graph_t** g, int** color_freq, int* n, int* m, int* k, int* c) {
	int l, i, j, d;
	if (fscanf(stdin, "p %d %d %d %d\n", n, m, c, k) != 4) {
		ERROR("invalid parameter line");
	}

	if (*n < 1 ||
			*n > 1000 ||
			*m < 1 ||
			*m > ((*n)*(*n-1))/2 ||
			*c < 1 ||
			*c > *n ||
			*k < 2 ||
			*k > 30)
		ERROR("invalid input parameters (n = %d, m = %d, c = %d, k = %d)",
				*n, *m, *c, *k);

	graph_alloc(g, *n);

	for (l = 0; l < *m; l++) {
		skipws(stdin);

		if (fscanf(stdin, "e %d %d\n", &i, &j) != 2) {
			ERROR("invalid edge line");
		}

		if (i < 1 || i > *n || i == j || j < 1 || j > *n) {
			ERROR("invalid edge (i = %d, j = %d)", i, j);
		}

		graph_add_edge(*g, i-1, j-1);
	}

	for (l = 0; l < *n; l++) {
		skipws(stdin);

		if (fscanf(stdin, "c %d %d\n", &i, &d) != 2) {
			ERROR("invalid color line");
		}

		if (i < 1 || i > *n || d < 1 || d > *c) {
			ERROR("invalid color (i = %d, d = %d)", i, d);
		}

		graph_set_color(*g, i-1, d-1);
	}

	*color_freq = (int*) MALLOC(sizeof(int)*(*c));

	for (l = 0; l < *c; l++) {
		(*color_freq)[l] = 0;
	}

	skipws(stdin);

	for (l = 0; l < *k; l++) {
		if (l == 0) {
			if (fscanf(stdin, "f %d", &d) != 1) {
				ERROR("invalid motif line");
			}
		}
		else {
			if (fscanf(stdin, " %d", &d) != 1) {
				ERROR("invalid motif line");
			}
		}

		if (d < 1 || d > *c) {
			ERROR("invalid motif component (d = %d)\n", d);
		}

		(*color_freq)[d-1]++;
	}
}

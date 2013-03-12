#ifndef GUARD_READER__
#define GUARD_READER__

#include <assert.h>
#include <ctype.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
	int num_vertices;
	int num_edges;
	int edge_capacity;
	int* edges;
	int* colors;
} graph_t;

#define ERROR(...) error(__FILE__,__LINE__,__func__,__VA_ARGS__);
#define MALLOC(x) malloc_wrapper(x)
#define FREE(x) free_wrapper(x)
void free_wrapper(void* p);

void skipws(FILE* in);
void graph_alloc(graph_t** g, int n);
void graph_free(graph_t* g);
void graph_add_edge(graph_t* g, int u, int v);
void graph_set_color(graph_t* g, int u, int c);
void graph_read(graph_t** g, int** color_freq, int* n, int* m, int* k, int* c);
void graph_print(graph_t* g, int* color_freq, int num_colors);

#endif

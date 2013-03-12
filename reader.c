
/*********************************************** Simple input format reader. */

/* 
 * Description: 
 *   
 *   Reads input from stdin (zero or more instances in succession), 
 *   prints what it read to stdout. 
 *
 * To compile (e.g. with gcc): 
 *
 *   gcc -o reader -Wall -O3 reader.c
 *
 * Example usage:
 *
 *   cat ../examples/example-input.txt | ./reader
 *
 */

#include<stdio.h>
#include<stdlib.h>
#include<stdarg.h>
#include<assert.h>
#include<ctype.h>

/************************************************** Some helper subroutines. */

#define ERROR(...) error(__FILE__,__LINE__,__func__,__VA_ARGS__);

static void error(const char *fn, int line, const char *func, 
                  const char *format, ...)
{
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

#define MALLOC(x) malloc_wrapper(x)
#define FREE(x) free_wrapper(x)

int malloc_balance = 0;

static void *malloc_wrapper(size_t size)
{
    void *p = malloc(size);
    if(p == NULL)
        ERROR("malloc fails");
    malloc_balance++;
    return p;
}

static void free_wrapper(void *p)
{
    free(p);
    malloc_balance--;
}

/************************************************ Rudimentary graph builder. */

typedef struct 
{
    int num_vertices;
    int num_edges;
    int edge_capacity;
    int *edges;
    int *colors;
} graph_t;

static int *enlarge(int m, int m_was, int *was)
{
    assert(m >= 0 && m_was >= 0);

    int *a = (int *) MALLOC(sizeof(int)*m);
    int i;
    if(was != (void *) 0) {
        for(i = 0; i < m_was; i++) {
            a[i] = was[i];
        }
        FREE(was);
    }
    return a;
}

graph_t *graph_alloc(int n)
{
    assert(n >= 0);

    int i;
    graph_t *g = (graph_t *) MALLOC(sizeof(graph_t));
    g->num_vertices = n;
    g->num_edges = 0;
    g->edge_capacity = 100;
    g->edges = enlarge(2*g->edge_capacity, 0, (void *) 0);
    g->colors = (int *) MALLOC(sizeof(int)*n);
    for(i = 0; i < n; i++)
        g->colors[i] = 0;
    return g;
}

void graph_free(graph_t *g)
{
    FREE(g->edges);
    FREE(g->colors);
    FREE(g);
}

void graph_add_edge(graph_t *g, int u, int v)
{
    assert(u >= 0 && 
           v >= 0 && 
           u != v && 
           u < g->num_vertices &&
           v < g->num_vertices);

    if(g->num_edges == g->edge_capacity) {
        g->edges = enlarge(4*g->edge_capacity, 2*g->edge_capacity, g->edges);
        g->edge_capacity *= 2;
    }

    assert(g->num_edges < g->edge_capacity);

    int *e = g->edges + 2*g->num_edges;
    g->num_edges++;
    e[0] = u;
    e[1] = v;
}

void graph_set_color(graph_t *g, int u, int c)
{
    assert(u >= 0 && u < g->num_vertices && c >= 0);
    g->colors[u] = c;
}

/********************************************* Skip whitespace and comments. */

void skipws(FILE *in)
{
    int c;
    do {
        c = fgetc(in);
        if(c == '#') {
            do {
                c = fgetc(in);
            } while(c != EOF && c != '\n');
        }
    } while(c != EOF && isspace(c));
    if(c != EOF)
        ungetc(c, in);
}

/****************************************************** Program entry point. */

int main(int argc, char **argv)
{
    int save_bal = malloc_balance;
    int n, m, c, k;
    int i, j, d, l;
    graph_t *g;
    int *color_freq;

    skipws(stdin);
    while(!feof(stdin)) {

        /* Read graph from stdin. */

        if(fscanf(stdin, "p %d %d %d %d\n", &n, &m, &c, &k) != 4)
            ERROR("invalid parameter line");
        if(n < 1 || 
           n > 1000 ||
           m < 1 ||
           m > (n*(n-1))/2 ||
           c < 1 ||
           c > n ||
           k < 2 ||
           k > 30)
            ERROR("invalid input parameters (n = %d, m = %d, c = %d, k = %d)",
                  n, m, c, k);
        
        g = graph_alloc(n);
        
        for(l = 0; l < m; l++) {
            skipws(stdin);
            if(fscanf(stdin, "e %d %d\n", &i, &j) != 2)
                ERROR("invalid edge line");
            if(i < 1 || i > n || i == j || j < 1 || j > n)
                ERROR("invalid edge (i = %d, j = %d)", i, j);
            graph_add_edge(g, i-1, j-1);
        }

        for(l = 0; l < n; l++) {
            skipws(stdin);
            if(fscanf(stdin, "c %d %d\n", &i, &d) != 2)
                ERROR("invalid color line");
            if(i < 1 || i > n || d < 1 || d > c)
                ERROR("invalid color (i = %d, d = %d)", i, d);
            graph_set_color(g, i-1, d-1);
        }
        
        color_freq = (int *) MALLOC(sizeof(int)*c);
        for(l = 0; l < c; l++)
            color_freq[l] = 0;

        skipws(stdin);
        for(l = 0; l < k; l++) {
            if(l == 0) {
                if(fscanf(stdin, "f %d", &d) != 1)
                    ERROR("invalid motif line");
            } else {
                if(fscanf(stdin, " %d", &d) != 1)
                    ERROR("invalid motif line");
            }
            if(d < 1 || d > c)
                ERROR("invalid motif component (d = %d)\n", d);
            color_freq[d-1]++;
        }

        /* Print out what we just read in. */
        fprintf(stdout, 
                "parameters: n = %d, m = %d, c = %d, k = %d\n",
                n, m, c, k);
        for(i = 0; i < m; i++)
            fprintf(stdout, 
                    "%s{%d,%d}",
                    i == 0 ? "edge list: " : " ",
                    g->edges[2*i+0] + 1,
                    g->edges[2*i+1] + 1);
        fprintf(stdout, "\n");      
        fprintf(stdout, "coloring [vertex (color)]:");
        for(i = 0; i < n; i++)
            fprintf(stdout, " %d(%d)", i, g->colors[i]);
        fprintf(stdout, "\n");      
        fprintf(stdout, "motif [color (frequency)]:");
        for(i = 0; i < c; i++)
            fprintf(stdout, " %d(%d)", i, color_freq[i]);
        fprintf(stdout, "\n");      
        fflush(stdout);

        /* Release memory & consider next graph. */
        FREE(color_freq);
        graph_free(g);

        skipws(stdin);
    }

    assert(save_bal == malloc_balance);

    return 0;
}

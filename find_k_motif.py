#! /usr/bin/python2
# vim: set fileencoding=utf-8
import fileinput
from reader import graphs_read
from gf2q import gf2q_rand, gf2q_add, gf2q_mul


def compute_generating_polynomial(g, x, y):
    previous = {}
    current = {}
    list_of_nodes = [r for r in g.items() if type(r[0]) == int]
    for (node, info) in list_of_nodes:
        previous[node] = x[node-1]

    k = len(g["motif"])
    for l in range(2, k+1):
        for (node, info) in list_of_nodes:
            current[node] = 0
            for neighbor in info[1]:
                edge_index = g["edges"][(min(neighbor, node),
                                         max(neighbor, node))]
                prod = gf2q_mul(x[node-1], y[edge_index])
                prod = gf2q_mul(prod, previous[neighbor])
                current[node] = gf2q_add(current[node], prod)

        previous = current

    res = 0
    for (node, info) in list_of_nodes:
        res = gf2q_add(res, current[node])

    return res


if __name__ == "__main__":
    for g in graphs_read(fileinput.input()):
        x = [gf2q_rand() for i in range(g["num_vertices"])]
        y = [gf2q_rand() for i in range(g["num_edges"])]
        print([r for r in g.items() if type(r[0]) == str])
        print(compute_generating_polynomial(g, x, y))

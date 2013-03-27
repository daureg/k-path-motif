#! /usr/bin/python2
# vim: set fileencoding=utf-8
# import pycallgraph
from heapq import heappush, heappop
from itertools import count
import random
from reader import graphs_read, CNodes
from time import clock
random.seed(13572)


def remove_one_color(full, one):
    if one not in full:
        return full
    pos = full.index(one)
    return full[:pos]+full[pos+1:]


def find_k_path(g):
    graph = g
    F = g["motif"]
    k = len(F)
    lo = k*[-1]

    def simplify():
        motif = graph["motif"]
        list_of_nodes = [n for n in graph.items() if type(n[0]) == int]
        removed = []
        for label, node_info in list_of_nodes:
            # remove 0-degree nodes and those whose color is not in motif
            if node_info.color not in motif or len(node_info.neighbors) == 0:
                graph.pop(label)
                removed.append(label)

        if len(removed) > 0:
            graph["nodes"] -= set(removed)
            graph["num_vertices"] -= len(removed)
            for label in graph["nodes"]:
                graph[label] = CNodes(graph[label].color,
                                      [n for n in graph[label].neighbors
                                       if n not in removed])

    def next_neighbors(nodes, path, motif):
        if path == []:
            return [], []
        forward = [n for n in graph[path[-1]].neighbors if n in nodes
                   and graph[n].color in motif]
        backward = [n for n in graph[path[0]].neighbors if n in nodes
                    and graph[n].color in motif]
        return forward, backward

    def branch(motif, nodes, path):
        k = len(g['motif'])
        # print len(motif), len(nodes), len(path)
        # abort early if there is no more hope
        if len(nodes) < len(motif):
            return
        if len(path) > k or (len(nodes) == 0 and len(path) < k):
            return

        if len(path) > len([i for i in lo if i != -1]):
            for k, n in enumerate(path):
                lo[k] = n

        if len(nodes) == 0:
            return

        f, b = next_neighbors(nodes, path, motif)
        alt = []
        for v in random.sample(f, min(len(f), len(f)/3+1)):
            p = path + [v]
            n = nodes - set([v])
            m = remove_one_color(motif, graph[v].color)
            alt.extend([(m, n, p), (motif, n, path)])
        for v in random.sample(b, min(len(b)/3+1, len(b))):
            p = [v] + path
            n = nodes - set([v])
            m = remove_one_color(motif, graph[v].color)
            alt.extend([(m, n, p), (motif, n, path)])

        if path == []:
            v = random.choice(list(nodes))
            p = [v]
            n = nodes - set([v])
            m = remove_one_color(motif, graph[v].color)
            alt.extend([(m, n, p), (motif, n, path)])

        for m, n, p in alt:
            # it seems logical that the color filtering is more efficient when
            # done in next_neighbors because it occurs less often
            yield len(p), branch(m, n, p)

    simplify()
    num = count()                                 # Helps avoid heap collisions
    Q = [(0, next(num),                           # Start with just the root
          branch(F, g["nodes"], []))]
    while Q:                                      # Any nodes left?
        _, _, r = heappop(Q)                      # Get one
        for b, u in r:                            # Expand it ...
            heappush(Q, (b, next(num), u))        # ... and push the children

    solution = [i for i in lo if i >= 0]
    if len(solution) > 0 and not solution[0] < solution[-1]:
        solution.reverse()

    return len(solution) == k, solution      # Return the solution

graph = {}
ograph = {}
all_inputs = ['example-input', 'no-16-6-1x6', 'no-16-6-2x3', 'no-16-7-1x7',
              'unique-16-6-1x6',
              # 'unique-16-6-2x3',
              'unique-16-7-1x7',
              'complete8', 'tenstars', 'small-no']

# all_inputs = [all_inputs[0]]
for testcase in all_inputs:
    with open(testcase+'.txt') as f:
        raw = f.readlines()

    for graph in graphs_read(raw):
        # pycallgraph.start_trace()
        print testcase
        for i in range(1):
            random.seed(13572)
            t0 = clock()
            exist, path = find_k_path(graph)
            print "{}:{:.3f}s".format(i, clock() - t0)
        print "{}{}".format("yes " if exist else "no",
                            " ".join(map(str, path)) if exist else "")
        # pycallgraph.make_dot_graph('star_wars.png')

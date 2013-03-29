#! /usr/bin/python2
# vim: set fileencoding=utf-8
# import pycallgraph
from heapq import heappush, heappop
from itertools import count
import random
from reader import graphs_read
from time import clock


def remove_one_color(motif, color):
    pos = motif.index(color)
    return motif[:pos]+motif[pos+1:]


def find_k_path(g):
    graph = g
    F = g["motif"]
    k = len(F)

    def remaining_motif(path):
        motif = g["motif"]
        for node in path:
            motif = remove_one_color(motif, g[node].color)
        return motif

    def complete_path(path):
        if len(path) < k-1:
            return path
        last_color = remaining_motif(path)
        f, b = next_neighbors(last_color, g["nodes"] - set(path), path)
        for node in f:
            if g[node].color == last_color[0]:
                return path + [node]
        for node in b:
            if g[node].color == last_color[0]:
                return [node] + path
        return path

    def find_sub_path(nodes, initial_guess):
        num = count()
        Q = [(0, next(num), branch(remaining_motif(initial_guess),
                                   nodes, initial_guess))]
        keep = []
        while Q:
            _, _, r = heappop(Q)
            for b, u, p, s in r:
                keep = p
                heappush(Q, (b, next(num), u))

        solution = complete_path(keep)
        if len(solution) > 0 and not solution[0] < solution[-1]:
            solution.reverse()

        return len(solution) == k, solution

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
                graph[label].neighbors = [n for n in graph[label].neighbors
                                          if n not in removed]

    def next_neighbors(motif, nodes, path):
        if path == []:
            return [], []
        forward = [n for n in graph[path[-1]].neighbors if n in nodes
                   and graph[n].color in motif]
        backward = [n for n in graph[path[0]].neighbors if n in nodes
                    and graph[n].color in motif]
        return forward, backward

    def branch(motif, nodes, path):
        k = len(g['motif'])
        # abort early if there is no more hope
        if len(nodes) < len(motif):
            return
        if len(path) > k or (len(nodes) == 0 and len(path) < k):
            return

        if len(nodes) == 0:
            return

        f, b = next_neighbors(motif, nodes, path)
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
            yield len(p), branch(m, n, p), p, n

    simplify()
    # for l, b, p, s in branch(F, g["nodes"], [], True):
    #     for _, _, np, ns in b:
    #         print '{}: {} -> {} {}'.format(l, p, np, ns)
    return find_sub_path(g["nodes"], [])

graph = {}
ograph = {}
all_inputs = ['example-input', 'no-16-6-1x6', 'no-16-6-2x3', 'no-16-7-1x7',
              'unique-16-6-1x6',
              # 'unique-16-6-2x3',
              'unique-16-7-1x7',
              'complete8', 'tenstars', 'small-no']

all_inputs = [all_inputs[0]]
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

#! /usr/bin/python2
# vim: set fileencoding=utf-8
from heapq import heappush, heappop
from itertools import count
from random import choice, sample, seed
from reader import graphs_read
from time import clock
from multiprocessing import Process, Queue
import sys

MULTI = '-s' not in sys.argv
# seed = lambda x: None


def remove_one_color(motif, color):
    pos = motif.index(color)
    return motif[:pos]+motif[pos+1:]


def find_k_path(msg, g, remaining=None, path=None):
    graph = g

    def remaining_motif(path):
        motif = g["motif"]
        for node in path:
            motif = remove_one_color(motif, g[node].color)
        return motif

    def find_sub_path(nodes, initial_guess):
        num = count()
        k = len(g['motif'])
        Q = [(k+1-len(initial_guess), next(num),
              branch(remaining_motif(initial_guess), nodes, initial_guess))]
        # print "push\t{} ({})".format(k+1, 0)
        solution = []
        done = False
        while Q and not done:
            l, _, r = heappop(Q)
            # print "POP\t{} ({})".format(l, -l+k+1)
            for l, u, p, _ in r:
                if len(p) == k:
                    solution = p
                    done = True
                    # print "done"
                    break
                heappush(Q, (l, next(num), u))
                # print "push\t{} ({})".format(l, -l+k+1)

        if len(solution) > 0 and not solution[0] < solution[-1]:
            solution.reverse()

        return len(solution) == k, solution

    def simplify():
        motif = graph["motif"]
        list_of_nodes = [n for n in graph.items() if type(n[0]) == int]
        removed = []
        for label, node_info in list_of_nodes:
            graph[label].neighbors = set(graph[label].neighbors)
            # remove 0-degree nodes and those whose color is not in motif
            if node_info.color not in motif or len(node_info.neighbors) == 0:
                graph.pop(label)
                removed.append(label)

        if len(removed) > 0:
            removed = set(removed)
            graph["nodes"] -= removed
            graph["num_vertices"] -= len(removed)
            for label in graph["nodes"]:
                graph[label].neighbors -= removed

    def next_neighbors(motif, nodes, path):
        if path == []:
            return [], []
        forward = [n for n in graph[path[-1]].neighbors if n in nodes
                   and graph[n].color in motif]
        backward = [n for n in graph[path[0]].neighbors if n in nodes
                    and graph[n].color in motif]
        return forward, backward

    def some_neighbors(all, fraction=0.33):
        return sample(all, min(len(all), int(len(all)*fraction+1)))

    def build_alternatives(path, old_nodes, new_node, motif, forward=True):
        p = path + [new_node] if forward else [new_node] + path
        n = old_nodes - set([new_node])
        m = remove_one_color(motif, graph[new_node].color)
        return [(m, n, p), (motif, n, path)]

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

        for v in some_neighbors(f):
            alt.extend(build_alternatives(path, nodes, v, motif))
        for v in some_neighbors(b):
            alt.extend(build_alternatives(path, nodes, v, motif, False))

        if path == []:
            v = choice(list(nodes))
            alt.extend(build_alternatives(path, nodes, v, motif))

        for m, n, p in alt:
            # it seems logical that the color filtering is more efficient when
            # done in next_neighbors because it occurs less often
            yield k+1-len(p), branch(m, n, p), p, n

    seed(13572)
    simplify()
    if msg is None:
        task = []
        for _, b, _, _ in branch(g["motif"], g["nodes"], []):
            for _, _, p, n in b:
                task.append((n, p))
        return task

    else:
        remaining_nodes = remaining if remaining is not None else g["nodes"]
        initial_path = path if path is not None else []
        if MULTI:
            msg.put((find_sub_path(remaining_nodes, initial_path)))
        else:
            return find_sub_path(remaining_nodes, initial_path)

if __name__ == '__main__':
    all_inputs = ['example-input', 'no-16-6-1x6', 'no-16-6-2x3', 'no-16-7-1x7',
                  'unique-16-6-1x6',
                  'unique-16-6-2x3',
                  'unique-16-7-1x7',
                  'complete8', 'tenstars', 'small-no']

    # all_inputs = [all_inputs[-3]]
    for testcase in all_inputs:
        with open(testcase+'.txt') as f:
            raw = f.readlines()

        print testcase
        for graph in graphs_read(raw):
            for i in range(1):
                seed(13572)
                t0 = clock()

                if MULTI:
                    msg = Queue()
                    num_answer = 0
                    exist, path = False, []
                    pool = []
                    tasks = find_k_path(None, graph) if MULTI else []
                    if tasks == []:
                        tasks = [(graph['nodes'], [])]

                    for nodes, path in tasks:
                        pool.append(Process(target=find_k_path,
                                            args=(msg, graph, nodes, path)))
                    for p in pool:
                        p.start()

                    while True:
                        exist, path = msg.get()
                        num_answer += 1
                        if exist or num_answer == len(pool):
                            break

                    for p in pool:
                        p.terminate()
                else:
                    exist, path = find_k_path(0, graph)

                print "{}:{:.3f}s".format(i, clock() - t0)
            print "{}{}".format("yes " if exist else "no",
                                " ".join(map(str, path)) if exist else "")

#! /usr/bin/python2
# vim: set fileencoding=utf-8
import re
import fileinput


class CNodes():
    def __init__(self, color=-1, neighbors=None):
        self.color = color
        self.neighbors = [] if neighbors is None else neighbors

    def __repr__(self):
        return '{}({})'.format(self.color, ','.join(map(str, self.neighbors)))


def graphs_read(text, directed=False):
    graph = {}
    no_edges = 0
    for line in text:
        line = line.strip()
        if line[0] == '#':
            continue

        params = map(int, re.split(r'\s+', line[1:].lstrip(' \t\n\r')))
        if line[0] == 'p':
            if len(params) != 4:
                raise ValueError("invalid parameters: {}".format(str(params)))

            n = params[0] if (1 <= params[0] <= 1000) else False
            m = params[1] if (1 <= params[1] <= (n*(n-1))/2) else False
            c = params[2] if (1 <= params[2] <= n) else False
            k = params[3] if (2 <= params[3] <= 30) else False
            if not (n and m and c and k):
                raise ValueError("invalid parameters: {}".format(str(params)))

            graph["num_vertices"] = n
            graph["num_edges"] = m
            graph["num_colors"] = c
            graph["edges"] = {}
            graph["nodes"] = set(range(1, n+1))
            for i in range(1, n+1):
                graph[i] = (0, [])
                graph[str(i)] = CNodes()

        if line[0] == 'e':
            if len(params) != 2:
                raise ValueError("invalid edge: {}".format(line))

            i = params[0]
            j = params[1]
            if i < 1 or i > n or i == j or j < 1 or j > n:
                raise ValueError("invalid edge: {}".format(line))

            if directed:
                graph[i][1].append(j)
                graph["edges"][(i, j)] = no_edges
            else:
                graph[i][1].append(j)
                graph[j][1].append(i)
                graph[str(i)].neighbors.append(j)
                graph[str(j)].neighbors.append(i)
                # graph["edges"][(min(i, j), max(i, j))] = no_edges

            no_edges += 1

        if line[0] == 'c':
            if len(params) != 2:
                raise ValueError("invalid color: {}".format(line))

            i = params[0]
            d = params[1]
            if i < 1 or i > n or d < 1 or d > c:
                raise ValueError("invalid color: {}".format(line))

            graph[i] = (d, graph[i][1])
            graph[str(i)].color = d

        if line[0] == 'f':
            if len(params) != k:
                raise ValueError("invalid motif: {}".format(line))

            graph["motif"] = sorted(params)
            if graph["motif"][0] < 0 or graph["motif"][-1] > c:
                raise ValueError("invalid motif: {}".format(line))

            yield graph


if __name__ == "__main__":
    for g in graphs_read(fileinput.input()):
        print(g["num_vertices"])

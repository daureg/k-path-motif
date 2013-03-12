#! /usr/bin/python2
# vim: set fileencoding=utf-8
import re
import fileinput


def graphs_read(text):
    graph = {}
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
            for i in range(1, n+1):
                graph[i] = (0, [])

        if line[0] == 'e':
            if len(params) != 2:
                raise ValueError("invalid edge: {}".format(line))

            i = params[0]
            j = params[1]
            if i < 1 or i > n or i == j or j < 1 or j > n:
                raise ValueError("invalid edge: {}".format(line))

            graph[i][1].append(j)
            graph[j][1].append(i)

        if line[0] == 'c':
            if len(params) != 2:
                raise ValueError("invalid color: {}".format(line))

            i = params[0]
            d = params[1]
            if i < 1 or i > n or d < 1 or d > c:
                raise ValueError("invalid color: {}".format(line))

            graph[i] = (d, graph[i][1])

        if line[0] == 'f':
            if len(params) != k:
                raise ValueError("invalid motif: {}".format(line))

            graph["motif"] = sorted(params)  # O(k ln k)
            if graph["motif"][0] < 0 or graph["motif"][-1] > c:
                raise ValueError("invalid motif: {}".format(line))

            yield graph


if __name__ == "__main__":
    for g in graphs_read(fileinput.input()):
        print(g["num_vertices"])

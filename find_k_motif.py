#! /usr/bin/python2
# vim: set fileencoding=utf-8
#import fileinput
from itertools import combinations, chain, groupby
from reader import graphs_read
from gf2q import gf2q_rand, gf2q_add, gf2q_mul


def powerset(n):
    """Generate all but the empty subsets of [1, ..., n]"""
    # from http://docs.python.org/2/library/itertools.html
    s = range(1, n+1)
    return chain.from_iterable(
        combinations(s, r) for r in range(1, len(s)+1))


def some_subsets(k, n):
    """Return the next k subsets of the powerset of [1,n]."""
    r = []
    for i, s in enumerate(powerset(n)):
        r.append(s)
        if (i+1) % k == 0 or i == (1 << n) - 2:
            yield r
            r = []


def all_walks(k, g):
    list_of_nodes = [r for r in g.items() if type(r[0]) == int]
    r = []
    for (node, info) in list_of_nodes:
        r += [w for w in all_walks_starting_from(node, k, g) if w[0] <= w[-1]]
        # r += all_walks_starting_from(node, k, g)

    return r


def all_walks_starting_from(u, k, g):
    """ Return all the walk of length k in g starting from node u.
    Use node's index (and not node's label)."""
    if k == 1:
        return [(u-1,)]

    r = []
    for neighbor in g[u][1]:
        edge_index = g["edges"][(min(neighbor, u),
                                 max(neighbor, u))]
        for walk in all_walks_starting_from(neighbor, k-1, g):
            r.append((u-1, edge_index)+walk)

    return r


def brutally_compute_generating_polynomial(g, x, y, allofthem=None):
    r = 0
    k = len(g["motif"])
    lw = allofthem
    if not lw:
        lw = all_walks(k, g)

    for walk in lw:
        r ^= monomial(walk, x, y)

    return r


def monomial(walk, x, y):
    r = 1
    for pos, number in enumerate(walk):
        factor = x[number] if pos % 2 == 0 else y[number]
        r = gf2q_mul(r, factor)

    return r


def pr_prev(previous, l):
    pr = []
    for u in range(len(previous)):
        pr.append("T[{}, {}]={}".format(u+1, l-1, previous[u]))

    # print("\t".join(pr))


def compute_generating_polynomial(g, x, y, k=-1):
    list_of_nodes = [r for r in g.items() if type(r[0]) == int]
    previous = len(list_of_nodes)*[0]
    current = len(list_of_nodes)*[0]
    for (node, info) in list_of_nodes:
        previous[node-1] = x[node-1]

    k = len(g["motif"]) if k == -1 else k
    for l in range(2, k+1):
        current = len(list_of_nodes)*[0]
        pr_prev(previous, l)
        for (node, info) in list_of_nodes:
            for neighbor in info[1]:
                edge = (min(neighbor, node), max(neighbor, node))
                edge_index = g["edges"][edge]
                prod = gf2q_mul(x[node-1], y[edge_index])
                cop = previous[neighbor-1]
                prod = gf2q_mul(prod, cop)
                current[node-1] = gf2q_add(current[node-1], prod)

        previous = current

    res = 0
    pr_prev(previous, k)
    # print('({}).integer_representation'.format(
    #     '+'.join(map(lambda x: "k.fetch_int({})".format(x), current))))
    for (node, info) in list_of_nodes:
        res = gf2q_add(res, current[node-1])

    return res


def is_path(walk):
    uniq = []
    for v in range(0, len(walk), 2):
        if walk[v] not in uniq:
            uniq.append(walk[v])
        else:
            return False

    return True


def solve(g, walks):
    for w in walks:
        if not is_path(w):
            continue

        m = []
        for c in g["motif"]:
            m.append(c)

        for v in range(0, 2*len(m), 2):
            node = w[v]+1
            color = g[node][0]
            if color in m:
                del m[m.index(color)]
            else:
                continue

        if m == []:
            p = [str(v+1) for i, v in enumerate(w) if i % 2 == 0]
            return "yes "+' '.join(p)

    return "no"


def walk_to_nodes(w):
    r = ""
    for pos, val in enumerate(w):
        if pos % 2 == 0:
            r += str(val+1)

    return r


if __name__ == "__main__":
    exe = ['example-input', 'no-16-6-2x3.txt']
    with open(exe[0]+'.txt') as f:
        graph = f.readlines()

    #for g in graphs_read(fileinput.input()):
    for g in graphs_read(graph):
        k = len(g["motif"])
        n = g["num_vertices"]
        c = g["num_colors"]
        colors = range(1, c+1)
        list_of_nodes = [r for r in g.items() if type(r[0]) == int]
# http://www.techrepublic.com/article/run-length-encoding-in-python/6310674
        present_shades = [len(list(multiplicity)) for color, multiplicity
                          in groupby(g["motif"])]
        shades = []
        index_shade = 0
        for col in colors:
            if col in g["motif"]:
                shades.append(present_shades[index_shade])
                index_shade += 1
            else:
                shades.append(0)

        Z = n*[[]]
        for (node, info) in list_of_nodes:
            Z[node-1] = [gf2q_rand() for s in range(shades[info[0]-1])]

        W = c*[[]]
        for u in colors:
            for s in range(shades[u-1]):
                W[u-1].append([gf2q_rand() for l in range(k)])

        y = [gf2q_rand() for i in range(g["num_edges"])]
        y = [1 for i in range(g["num_edges"])]
        # lw = all_walks(k, g)
        # for i in range(6):
        #     y = [gf2q_rand() for i in range(g["num_edges"])]
        #     x = [gf2q_rand() for i in range(n)]
        #     print('{}\t{}'.format(compute_generating_polynomial(g, x, y),
        #     brutally_compute_generating_polynomial(g, x, y, lw)))
        lw = all_walks(k, g)
        # print(solve(g, lw))
        total = 0
        ps = list(powerset(k))
        for A in ps[:-1]:
            x = n*[0]
            for i in range(n):
                i_color = g[i+1][0]-1
                for l in A:
                    for s in range(shades[i_color]):
                        x[i] ^= gf2q_mul(Z[i][s], W[i_color][s][l-1])

            a = brutally_compute_generating_polynomial(g, x, y, lw[0:1])
            #a = compute_generating_polynomial(g, x, y)
            # if len(A) % 3 == 0:
            print(total, a)

            total ^= a

        x = n*[0]
        for i in range(n):
            i_color = g[i+1][0]-1
            for l in range(k):
                for s in range(shades[i_color]):
                    x[i] ^= gf2q_mul(Z[i][s], W[i_color][s][l-1])

        print(total)
        print(brutally_compute_generating_polynomial(g, x, y, lw[0:1]))

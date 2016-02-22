#%%

import numpy
import networkx

G = networkx.MultiGraph()
edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
         (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
         (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
         (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
         (1, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]
#edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
#         (0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 1 })]

G.add_edges_from(edges)

start = 0
end = 3

# For each edge there is flow * c(flow). These are the edgeFuncs. The global
#   optimizer minimizes the sum of these functions
cost = [lambda x : x, lambda x : 1, lambda x : 0]
tax = [lambda x : 0, lambda x : 0, lambda x : 0]

N = 100

R = 10

preferences = {}
edgeResults = {}
totals = []

for i in range(N):
    for n1 in G.edge:
        for n2 in G.edge[n1]:
            for en in G.edge[n1][n2]:
                preferences[(i, n1, n2, en)] = numpy.random.exponential()

for r in range(R):
    for n1 in G.edge:
        for n2 in G.edge[n1]:
            for en in G.edge[n1][n2]:
                G.edge[n1][n2][en]['f'] = 0.0

    order = range(N)
    numpy.random.shuffle(order)
    for i in order:
        for n1 in G.edge:
            for n2 in G.edge[n1]:
                for en in G.edge[n1][n2]:
                    G.edge[n1][n2][en]['c'] = cost[G.edge[n1][n2][en]['t']](G.edge[n1][n2][en]['f']) + \
                                        tax[G.edge[n1][n2][en]['t']](G.edge[n1][n2][en]['f']) + \
                                        preferences[(i, n1, n2, en)]

        path = networkx.shortest_path(G, source = start, target = end, weight = 'c')

        for n1, n2 in list(zip(path[:-1], path[1:])):
            sorted(G.edge[n1][n2].values(), key = lambda x : x['c'])[0]['f'] += 1.0 / N

    totalc = 0.0
    for n1, n2 in set(G.edges()):
        for edgeData in G.get_edge_data(n1, n2).values():
            key = (n1, n2, edgeData['t'])
            if key not in edgeResults:
                edgeResults[key] = []

            edgeResults[key].append(edgeData['f'])
            totalc += edgeData['f'] * cost[edgeData['t']](edgeData['f'])

    totals.append(totalc)


for (n1, n2, t), f in edgeResults.items():
    print u"Edge ({0}, {1}), type {2}, flow {3} \u00B1 {4}".format(n1, n2, t, numpy.mean(f), numpy.std(f))

print '----'
print u"Total cost: {0} \u00B1 {1}".format(numpy.mean(totals), numpy.std(totals))
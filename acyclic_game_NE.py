#%%

import numpy
import networkx



def runRound(G, start, end, cost, tax, bias, N): 

    # For each edge there is flow * c(flow). These are the edgeFuncs. The global
    #   optimizer minimizes the sum of these functions


    initial =True

    preferences = {}
    edgeResults = {}
    totals = []

    for i in range(N):
        for n1 in G.edge:
            for n2 in G.edge[n1]:
                for en in G.edge[n1][n2]:
                    preferences[(i, n1, n2, en)] = bias()

    #zero the graph edges to start
    for n1 in G.edge:
        for n2 in G.edge[n1]:
            for en in G.edge[n1][n2]:
                G.edge[n1][n2][en]['f'] = 0.0
                
    # we need to preserve the balance of edges at the end of the round. becuas I should change my mind just because the flow changed...
    # If I change my mind, remove myself from the previous
    # for r in range(R):
    aCur ={} # create 
    aPrev =None
    ct=0
    while ((initial or aCur != aPrev) and ct <100):
        ct+=1
        aPrev = dict(aCur)



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

            pEdge=list(zip(path[:-1], path[1:]))
            pEdge.sort()
            aCur[i] =pEdge
            if (not initial):
                if(aPrev[i] !=pEdge):
                    for eo, en in zip(aPrev[i],pEdge):
                        if (eo != en):
                            sorted(G.edge[en[0]][en[1]].values(), key = lambda x : x['c'])[0]['f'] += 1.0 / N
                            sorted(G.edge[eo[0]][eo[1]].values(), key = lambda x : x['c'])[0]['f'] -= 1.0 / N
                            print 'changed'
            else:
                for n1, n2 in pEdge: #loop over the path increasing flow
                    sorted(G.edge[n1][n2].values(), key = lambda x : x['c'])[0]['f'] += 1.0 / N

        initial =False  

    totalc = 0.0
    for n1, n2 in set(G.edges()):
        for edgeData in G.get_edge_data(n1, n2).values():
            key = (n1, n2, edgeData['t'])
            if key not in edgeResults:
                edgeResults[key] = []

            edgeResults[key].append(edgeData['f'])
            totalc += edgeData['f'] * cost[edgeData['t']](edgeData['f'])

    #totals.append(totalc)



    for (n1, n2, t), f in edgeResults.items():
        print u"Edge ({0}, {1}), type {2}, flow {3} \u00B1 {4}".format(n1, n2, t, numpy.mean(f), numpy.std(f))

    print '----'
    print u"Total cost: {0} \u00B1 {1}".format(numpy.mean(totalc), numpy.std(totalc))
    print 'Total iterations:', ct

bias =numpy.random.exponential
#bias = lambda : 0
G = networkx.MultiGraph()
edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
     (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
     (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
     (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
     (1, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]
#edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
#         (0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 1 })]

G.add_edges_from(edges)

cost = [lambda x : x, lambda x : 1.01, lambda x : 0]
tax = [lambda x : 0, lambda x : 0, lambda x : 0]

start = 0
end = 3

N = 100 #number of players
runRound(G, start, end, cost, tax, bias, N)
#%%

import numpy
import networkx


def runRound(edges, start, end, cost, tax, biases, N, debug = False):
    # For each edge there is flow * c(flow). These are the edgeFuncs. The global
    #   optimizer minimizes the sum of these functions

    initial =True

    preferences = {}
    edgeResults = {}

    # Add ids to every edge so that biases can be indexed
    for i, (n1, n2, edgeData) in enumerate(edges):
        edgeData['id'] = i

    G = networkx.Graph()
    G.add_edges_from(edges)

    #print G.edge
    #print G.edge[0]

    for i in range(N):
        for n1 in G.edge:
            for n2 in G.edge[n1]:
                preferences[(i, n1, n2)] = biases[G.edge[n1][n2]['t']](i)

    #zero the graph edges to start
    for n1 in G.edge:
        for n2 in G.edge[n1]:
            G.edge[n1][n2]['f'] = 0.0

    # we need to preserve the balance of edges at the end of the round. becuas I should change my mind just because the flow changed...
    # If I change my mind, remove myself from the previous
    # for r in range(R):
    aCur = {} # create
    aPrev = None
    ct = 0
    history = []
    backtrack = False
    totalc = 0.0
    edgeResults = {}
    maxIters = 10
    withV ={}
    while ((initial or aCur != aPrev) and ct < maxIters):
        ct += 1
        if aCur in history:
            backtrack=True
        history.append(dict(aCur))
        aPrev = dict(aCur)

        order = range(N)
        numpy.random.shuffle(order)
        setCost={}
        for i in order:
            if i in aPrev:
                for n1, n2 in aCur[i]:
                    G.edge[n1][n2]['f'] -= 1.0 / N
            edgeValueSettings=[]
            for n1 in G.edge:
                for n2 in G.edge[n1]:
                    G.edge[n1][n2]['c'] = cost[G.edge[n1][n2]['t']](G.edge[n1][n2]['f']) + \
                                            tax[G.edge[n1][n2]['t']](G.edge[n1][n2]['f']) + \
                                            preferences[(i, n1, n2)]
                    edgeValueSettings.append((G.edge[n1][n2]['c'], n1, n2))        
            setCost[i]=edgeValueSettings


            paths = networkx.all_simple_paths(G, source = start, target = end)

            pathCosts = []

            pathFlowsEst = []
            for path in paths:
                c = 0
                f=[]
                edges = zip(path[:-1], path[1:])

                for n0, n1 in edges:
                    c += G.edge[n0][n1]['c']
                    f.append((G.edge[n0][n1]['f'],
                              preferences[(i, n0, n1)],
                              cost[G.edge[n0][n1]['t']](G.edge[n0][n1]['f']),
                              tax[G.edge[n0][n1]['t']](G.edge[n0][n1]['f']),
                              G.edge[n0][n1]['c'],
                              n0,
                              n1)
                            )
                pathCosts.append((c, edges))
                pathFlowsEst.append((c,f,edges))

            pEdge = sorted(pathCosts, key = lambda x : x[0])[0][1]

            aCur[i] = pEdge

            withV[i] =(pEdge, pathFlowsEst)


            for n1, n2 in aCur[i]:
                G.edge[n1][n2]['f'] += 1.0 / N

            totalc = 0.0
            edgeResults = {}
            for n1, n2 in set(G.edges()):
                edgeData = G.edge[n1][n2]
                key = (n1, n2)

                edgeResults[key] = edgeData['f'], edgeData['t']
                totalc += edgeData['f'] * cost[edgeData['t']](edgeData['f'])


            if debug:
                for (n1, n2), (f, t) in edgeResults.items():
                    print u"Edge ({0}, {1}), type {2}, flow {3}".format(n1, n2, t, f)

                print '----'
                print u"Total cost: {0}".format(numpy.mean(totalc))
                print '****'

        initial = False

        if debug:
            print 'Total iterations:', ct

    if debug:
        if backtrack:
            print "Game is not potential game"
        else:
            print "No backtracking detected"

    nBC  = [(n, aCur[n], preferences[(n,0,1)],preferences[(n,0,2)]) for n in aCur]
    counts = [0,0,0,0,0,0,0,0]
    meanBias = [0,0]
    ct=0
    for i,p,p1,p2 in nBC:
        if p[0][1] ==1:
            meanBias[0]+=p1
            meanBias[1]+=p2
            ct+=1
    meanBias[0] /= 1.0*ct
    meanBias[1] /= 1.0*ct
    for i,p,p1,p2 in nBC:
        if p[0][1] ==1:
            if p1 <meanBias[0]:
                if p2 < meanBias[1]:
                    counts[0]+=1
                else:
                    counts[1]+=1
            else:
                if p2 < meanBias[1]:
                    counts[2]+=1
                else:
                    counts[3]+=1
        else:
            if p1 <meanBias[0]:
                if p2 < meanBias[1]:
                    counts[4]+=1
                else:
                    counts[5]+=1
            else:
                if p2 < meanBias[1]:
                    counts[6]+=1
                else:
                    counts[7]+=1
    print meanBias
    return totalc, edgeResults, backtrack, (ct < maxIters), counts, nBC, withV, preferences,setCost


if __name__ == '__main__':
    #bias = lambda : 0
    edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
         (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 2 }),
         (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 2 }),
         (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
         (1, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 0 })]
    #edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
    #         (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
    #         (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
    #         (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]

    bias = [lambda i : 0, lambda i : 0, lambda i : 0, lambda i : 0.0, lambda i : 0.0]#numpy.random.exponential

    cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
    tax = [lambda x : 0, lambda x : x, lambda x : 0]

    start = 0
    end = 3

    N = 100 #number of players
    print runRound(edges, start, end, cost, tax, bias, N, True)
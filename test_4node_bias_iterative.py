#%%

import acyclic_game_NE
import networkx
import numpy
import matplotlib.pyplot as plt
import itertools

reload(acyclic_game_NE)

#bias = lambda : 0
G = networkx.MultiDiGraph()
edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
     (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
     (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
     (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
     (1, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]
#,
 #    (2, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })
G.add_edges_from(edges)

cost = [lambda x : x, lambda x : 1.0, lambda x : 0]
tax = [lambda x : 0, lambda x : 0, lambda x : 0]

start = 0
end = 3

N = 100 #number of players

#%%
reload(acyclic_game_NE)
# Varying random bias on both roads
N = 100
for rngName, rng, biases in [('Exponential', lambda x : x * numpy.random.exponential(), numpy.linspace(0.0, 1.5, 11)),
                     ('Gaussian varying mean', lambda x : max(0.0, numpy.random.normal(loc = x, scale = 0.25)), numpy.linspace(0.0, 1.5, 11))]:

    for taxNumber in range(4):
        bs = []
        costs = []
        for b in biases:
            bias = []
            tmp1 = [rng(b) for i in range(N)]
            bias.append(lambda i : tmp1[i])
            tmp2 = [rng(b) for i in range(N)]
            bias.append(lambda i : tmp2[i])
            tmp3 = [rng(b) for i in range(N)]
            bias.append(lambda i : tmp3[i])
            tmp4 = [rng(b) for i in range(N)]
            bias.append(lambda i : tmp4[i])
            tmp5 = [rng(b) for i in range(N)]
            bias.append(lambda i : tmp5[i])
            tmp6 = [rng(b) for i in range(N)]
            bias.append(lambda i : tmp6[i])

            #bias[0] = lambda i : 0
            #bias[1] = lambda i : 0
            #bias[2] = lambda i : 0
            #bias[3] = lambda i : 0
            #bias[-1] = lambda i : 0

            if taxNumber == 0:
                tax = [lambda x : 0, lambda x : 0, lambda x : 0, lambda x : 0, lambda x : 0]
            elif taxNumber == 1:
                tax = [lambda x : x, lambda x : 0, lambda x : 0, lambda x : x, lambda x : 0]
            elif taxNumber == 2:
                tax = [lambda x : b, lambda x : b, lambda x : b, lambda x : b, lambda x : b, lambda x : b]
            else:
                tax = [lambda x : x + b, lambda x : b, lambda x : b, lambda x : x + b, lambda x : b, lambda x : b]

            rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

            bs.append(b)
            costs.append(rcost)

        plt.plot(bs, costs)
    plt.xlabel('Mean of bias distribution')
    plt.ylabel('Cost')
    plt.legend(['No taxes ({0})'.format(rngName), 'With Pigou taxes ({0})'.format(rngName), 'With bias taxes ({0})'.format(rngName), 'With both taxes'])
    plt.show()


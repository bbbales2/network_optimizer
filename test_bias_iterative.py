#%%

import acyclic_game_NE
import networkx
import numpy
import matplotlib.pyplot as plt

reload(acyclic_game_NE)

#bias = lambda : 0
G = networkx.MultiGraph()
#edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
#     (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
#     (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
#     (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
#     (1, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]
edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
         (0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 1 })]

G.add_edges_from(edges)

cost = [lambda x : x, lambda x : 1.0, lambda x : 0]
tax = [lambda x : 0, lambda x : 0, lambda x : 0]

start = 0
end = 1

N = 100 #number of players

bias = [lambda i : 0, lambda i : 0]#
print acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

xs = numpy.linspace(0, 1, 100)
plt.plot(xs, xs**2 + (1 - xs)**3)
plt.show()
#%%
x = 0.4514
print x**2 + (1 - x)**3
#%%
# Varying constant bias of road 2
for tax in ([lambda x : 0, lambda x : 0], [lambda x : x, lambda x : 0]):
    bs = []
    costs = []
    for b in numpy.linspace(0.0, 1.5, 15):
        bias = [lambda i : b, lambda i : 0]#
        rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

        bs.append(b)
        costs.append(rcost)

    plt.plot(bs, costs)
    plt.xlabel('Bias away from driving on road 1')
    plt.ylabel('Resultant cost')
    plt.title('Results given a constant bias')
plt.legend(['No taxes', 'With Pigou taxes'])
plt.show()

#%%
# Varying random bias of road 2
N = 100
for rngName, rng, biases in [('Exponential', lambda x : x * numpy.random.exponential(), numpy.linspace(0.0, 1.5, 11)),
                     ('Gaussian varying mean', lambda x : max(0.0, numpy.random.normal(loc = x, scale = 1.0)), numpy.linspace(0.0, 1.5, 11))]:
    for taxNumber in range(4):
        bs = []
        costs = []
        for b in biases:
            biases2 = [rng(b) for i in range(N)]

            bias = [lambda i : biases2[i], lambda i : 0]#
            if taxNumber == 0:
                tax = [lambda x : 0, lambda x : 0]
            elif taxNumber == 1:
                tax = [lambda x : x, lambda x : 0]
            elif taxNumber == 2:
                tax = [lambda x : b, lambda x : 0]
            else:
                tax = [lambda x : x + b, lambda x : 0]

            rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

            bs.append(b)
            costs.append(rcost)

        plt.plot(bs, costs)

    plt.xlabel('Average bias away from driving on road 1 for a given population')
    plt.ylabel('Resultant cost')
    plt.ylim(0.75, 1.01)
    plt.title('Results given a random ({0}) scaled bias to drive on road 2'.format(rngName))
    plt.legend(['No taxes', 'With Pigou taxes', 'With bias taxes', 'With both taxes'])
    plt.show()
##%%
## Varying random bias on both roads
#N = 1000
#bs = []
#costs = []
#for b in numpy.linspace(-0.5, 1.5, 11):
#    biases1 = [b * numpy.random.exponential() for i in range(N)]
#    biases2 = [b * numpy.random.exponential() for i in range(N)]
#    bias = [lambda i : biases1[i], lambda i : biases2[i]]#
#    rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)
#
#    bs.append(b)
#    costs.append(rcost)
#
#plt.plot(bs, costs)
#plt.xlabel('Average bias to drive on either road for a given population')
#plt.ylabel('Resultant cost')
#plt.title('Results given a random scaled bias to drive on both roads')
#plt.show()
#
#plt.hist(numpy.array(biases2) - numpy.array(biases1), bins = 25)
#plt.title('Histogram of biases to drive on road 2 vs. road 1 for average bias = {0}'.format(b))
#plt.show()


#%%
# Varying random bias on both roads
N = 100
for rngName, rng, biases in [('Exponential', lambda x : x * numpy.random.exponential(), numpy.linspace(0.0, 1.5, 11)),
                     ('Clamped > 0 gaussian w/ varying mean', lambda x : max(0.0, numpy.random.normal(loc = x, scale = 1.0)), numpy.linspace(0.0, 1.5, 11))]:

    for taxNumber in range(4):
        bs = []
        costs = []
        bs1 = biases
        bs2 = biases
        for b1 in bs1:
            for b2 in bs2:
                biases1 = [rng(b1) for i in range(N)]
                biases2 = [rng(b2) for i in range(N)]
                bias = [lambda i : biases1[i], lambda i : biases2[i]]#
                if taxNumber == 0:
                    tax = [lambda x : 0, lambda x : 0]
                elif taxNumber == 1:
                    tax = [lambda x : x, lambda x : 0]
                elif taxNumber == 2:
                    tax = [lambda x : b1, lambda x : b2]
                else:
                    tax = [lambda x : x + b1, lambda x : b2]

                rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

                costs.append(rcost)

        costs = numpy.array(costs).reshape(11, 11)

        plt.imshow(costs, interpolation = 'NONE', cmap = plt.cm.Greys, clim = [0.75, 1.0])
        plt.xticks(range(11), bs1)
        plt.yticks(range(11), bs2)
        plt.colorbar()
        plt.xlabel('Average bias away from road 1')
        plt.ylabel('Average bias away from road 2')
        plt.title(['No taxes ({0})'.format(rngName), 'With Pigou taxes ({0})'.format(rngName), 'With bias taxes ({0})'.format(rngName), 'With both taxes'][taxNumber])
        plt.show()


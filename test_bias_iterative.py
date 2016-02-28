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

cost = [lambda x : x, lambda x : 1.00, lambda x : 0]
tax = [lambda x : 0, lambda x : 0, lambda x : 0]

start = 0
end = 1

N = 100 #number of players

#%%
# Varying constant bias of road 2
bs = []
costs = []
for b in numpy.linspace(-0.5, 1.5, 11):
    bias = [lambda i : 0, lambda i : b]#
    rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

    bs.append(b)
    costs.append(rcost)

plt.plot(bs, costs)
plt.xlabel('Bias towards driving on road 2')
plt.ylabel('Resultant cost')
plt.title('Results given a constant bias')
plt.show()

#%%
# Varying random bias of road 2
N = 1000
bs = []
costs = []
for b in numpy.linspace(-0.5, 1.5, 11):
    biases = [b * numpy.random.exponential() for i in range(N)]
    bias = [lambda i : 0, lambda i : biases[i]]#
    rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

    bs.append(b)
    costs.append(rcost)

plt.plot(bs, costs)
plt.xlabel('Average bias to drive on road 2 for a given population')
plt.ylabel('Resultant cost')
plt.title('Results given a random scaled bias to drive on road 2')
plt.show()

plt.hist(numpy.array(biases), bins = 25)
plt.title('Histogram of biases to drive on road 2 for average bias = {0}'.format(b))
plt.show()
#%%
# Varying random bias on both roads
N = 1000
bs = []
costs = []
for b in numpy.linspace(-0.5, 1.5, 11):
    biases1 = [b * numpy.random.exponential() for i in range(N)]
    biases2 = [b * numpy.random.exponential() for i in range(N)]
    bias = [lambda i : biases1[i], lambda i : biases2[i]]#
    rcost, edgeResults, backtrack, converged = acyclic_game_NE.runRound(edges, start, end, cost, tax, bias, N)

    bs.append(b)
    costs.append(rcost)

plt.plot(bs, costs)
plt.xlabel('Average bias to drive on either road for a given population')
plt.ylabel('Resultant cost')
plt.title('Results given a random scaled bias to drive on both roads')
plt.show()

plt.hist(numpy.array(biases2) - numpy.array(biases1), bins = 25)
plt.title('Histogram of biases to drive on road 2 vs. road 1 for average bias = {0}'.format(b))
plt.show()

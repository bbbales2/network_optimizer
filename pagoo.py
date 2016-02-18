#%%
# This solves the network traffic for Nash and latency minimizing examples
#

import numpy
import cvxpy as cvx

# So you need to define the edges of your network, the start and stop nodes,
#   the integrals of the cost functions at each edge in the network, and the
#   cost function times the flow at each edge in the network

edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
#edges = [(0, 1), (0, 1)]

start = 0
end = 3

# We encode what function to use for the cost in the global and Nash problems
#   by providing for each edge an index into a list of functions (edgeFuncs and edgeIntFuncs)
edgeTypes = [0, 1, 1, 0]

# For each edge there is flow * c(flow). These are the edgeFuncs. The global
#   optimizer minimizes the sum of these functions
edgeFuncs = [lambda x : x**2, lambda x : x]

# For each edge there is a function integral(c(flow)) that represents the cost
#   that the Nash flow will minimize
edgeIntFuncs = [lambda x : 0.5 * x**2, lambda x : x]

####

signs = {}

nodes = {}
nodes = set(reduce(lambda x, y : x + y, edges))

A = numpy.zeros((len(nodes), len(edges)))

for e, edge in enumerate(edges):
    A[edge[0], e] = -1
    A[edge[1], e] = 1
    
b = numpy.zeros(len(nodes))

b[start] = -1
b[end] = 1

x = cvx.Variable(len(edges))

nash_obj = 0
global_obj = 0
for i, eType in enumerate(edgeTypes):
    nash_obj += edgeIntFuncs[eType](x[i])
    global_obj += edgeFuncs[eType](x[i])

nash_obj = cvx.Minimize(nash_obj)
global_obj = cvx.Minimize(global_obj)

constraints = [A * x - b == 0,
               x >= 0]

# I stole these prints from the CVXPY documentation!
prob = cvx.Problem(nash_obj, constraints)
prob.solve()
print "Nash solution"
print "status:", prob.status
print "optimal value", prob.value
print "optimal var", x.value, y.value

prob = cvx.Problem(global_obj, constraints)
prob.solve()
print "Global solution"
print "status:", prob.status
print "optimal value", prob.value
print "optimal var", x.value, y.value
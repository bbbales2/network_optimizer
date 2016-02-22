#%%
# This solves the network traffic for Nash and latency minimizing examples
#

import numpy
import cvxpy as cvx
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
# We encode what function to use for the cost in the global and Nash problems
#   by providing for each edge an index into a list of functions (edgeFuncs and edgeIntFuncs)
edgeTypes = [0, 1, 2, 2]

# For each edge there is flow * c(flow). These are the edgeFuncs. The global
#   optimizer minimizes the sum of these functions
edgeFuncs = [lambda x : x**2, lambda x : x, lambda x:0]

# For each edge there is a function integral(c(flow)) that represents the cost
#   that the Nash flow will minimize
edgeIntFuncs = [lambda x : 0.5 * x**2, lambda x : x, lambda x:0]

#Marginal Tax
edgeTaxIntFuncs = [lambda x : 0.5 * x**2, lambda x : 0, lambda x:0]


# So you need to define the edges of your network, the start and stop nodes,
#   the integrals of the cost functions at each edge in the network, and the
#   cost function times the flow at each edge in the network
def computeNE(edges, endpoints, edgeTypes, edgeFuncs,edgeIntFuncs, edgeTaxIntFuncs, edgeBiasFuncs):

	#edges = [(0, 1), (0, 1)]

	start = endpoints[0]
	end = endpoints[1]

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
	nash_tax_obj = 0
	global_obj = 0
	for i, eType in enumerate(edgeTypes):
	    nash_obj += edgeIntFuncs[eType](x[i])+edgeBiasFuncs[eType](x[i])
	    nash_tax_obj += edgeIntFuncs[eType](x[i]) + edgeTaxIntFuncs[eType](x[i])+edgeBiasFuncs[eType](x[i])
	    global_obj += edgeFuncs[eType](x[i])

	nash_obj = cvx.Minimize(nash_obj)
	nash_tax_obj = cvx.Minimize(nash_tax_obj)
	global_obj = cvx.Minimize(global_obj)

	constraints = [A * x - b == 0,
	               x >= 0]

	# I stole these prints from the CVXPY documentation!
	prob = cvx.Problem(nash_obj, constraints)
	prob.solve()
	'''	print "Nash solution"
	print "status:", prob.status
	print "optimal value", prob.value
	print "optimal var", x.value'''
	neOpt=x.value
	prob = cvx.Problem(nash_tax_obj, constraints)
	prob.solve()
	'''print "Global solution"
	print "status:", prob.status
	print "optimal value", prob.value
	print "optimal var", x.value'''
	neTaxOpt=x.value
	prob = cvx.Problem(global_obj, constraints)
	prob.solve()
	'''print "Global solution"
	print "status:", prob.status
	print "optimal value", prob.value
	print "optimal var", x.value'''

	ntotal = 0.0
	for i, f in enumerate(neOpt):
		ntotal += edgeFuncs[edgeTypes[i]](f)
	nTtotal = 0.0
	for i, f in enumerate(neTaxOpt):
		nTtotal += edgeFuncs[edgeTypes[i]](f)
	return (ntotal,nTtotal)

def makeBias(edges, emptyEdges):
	bias = []
	eVals= []
	for e in range(edges-emptyEdges):
		r = random.uniform(-2,2)
		bias.append(lambda x,r=r: -r*x)
		eVals.append(r)
	bias =bias+[lambda x: 0 for e in range(emptyEdges)]
	return (bias,eVals)
'''
def makeBiasGrid(dims, across):
	dim = tuple([across for d in dims])
	biasList = np.zeros(dim)
	for d in dims:
		for i in range(across):
'''

def makeBiasGrid(xDim, yDim, across):
	biasList = []
	for a in range(across):
		for b in range(across):
			biasList.append( [ lambda x,a=a: x*(xDim[0] +(xDim[1]-xDim[0])/float(across)*a), lambda x,b=b:(yDim[0] +(yDim[1]-yDim[0])/float(across)*b)*x, lambda x: 0 ] )
	return biasList
def makeGrid(xDim, yDim, across):
	biasList = []
	for a in range(across):
		for b in range(across):
			biasList.append( ( (xDim[0] +(xDim[1]-xDim[0])/float(across)*a),(yDim[0] +(yDim[1]-yDim[0])/float(across)*b) ) )
	return biasList
def runTest():
	bias,eVals = makeBias(3,1)
	print bias
	neOpt,neTaxOpt,gOpt=computeNE(edges,(0,3),edgeTypes,edgeFuncs,edgeIntFuncs,edgeTaxIntFuncs,bias)
	return (neOpt,neTaxOpt,gOpt, eVals)

def graphData():
	bound = (0,2)
	gridSize = 20
	biasEntries = makeBiasGrid(bound,bound, gridSize)
	biasGridPts = makeGrid(bound,bound,gridSize)

	data = [(biasGridPts[i], computeNE(edges,(0,3),edgeTypes,edgeFuncs,edgeIntFuncs,edgeTaxIntFuncs,bias)) for i,bias in enumerate(biasEntries) ]
	
	data1 = numpy.array([i[1][0] for i in data]).reshape(gridSize,gridSize)
	data2 = numpy.array([i[1][1] for i in data]).reshape(gridSize,gridSize)
	data3 = numpy.array([i[1][0]-i[1][1] for i in data]).reshape(gridSize,gridSize)
	
	return (data1,data2,data3)


#im is NxN

data = graphData()

fig =plt.figure()
ax1 = fig.add_subplot(131)
ax2=fig.add_subplot(132)
ax3=fig.add_subplot(133)
ax1.imshow(data[0], interpolation = 'NONE')#cmap = plt.cm.gray
ax2.imshow(data[1], interpolation = 'NONE')#cmap = plt.cm.gray
ax3.imshow(data[2], interpolation = 'NONE')#cmap = plt.cm.gray
#ax1.colorbar()
#fig.colorbar()


plt.show()


'''
ax = fig.add_subplot(131, projection='3d')
for i in data[0]:
	ax.scatter(i[0],i[1],i[2],c='r',marker='o')
ax.set_xlabel('Bias for top edge')
ax.set_ylabel('Bias for bottom edge')
ax.set_zlabel('Trafic on Edge 1')
bx = fig.add_subplot(132, projection='3d')
for i in data[1]:
	bx.scatter(i[0],i[1],i[2],c='r',marker='o')
bx.set_xlabel('Bias for top edge')
bx.set_ylabel('Bias for bottom edge')
bx.set_zlabel('Trafic on Edge 1')
cx = fig.add_subplot(133, projection='3d')
for i in data[2]:
	cx.scatter(i[0],i[1],i[2],c='r',marker='o')
cx.set_xlabel('Bias for top edge')
cx.set_ylabel('Bias for bottom edge')
cx.set_zlabel('Trafic on Edge 1')
plt.show()
'''
#%%
import game_NE
import numpy
import matplotlib.pyplot as plt

reload(game_NE)

edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
         (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
         (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
         (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]

distType = 'bernoulli'

def dist(p):
    if distType == 'bernoulli':
        return a if numpy.random.random() < p else b
    elif distType == 'exponential':
        return numpy.random.exponential(p + 1.0e-5)
    elif distType == 'normal':
        return numpy.random.normal(loc = p, scale = 0.1)
    else:
        raise Exception("Distribution {0} not found".format(distType))

a = 1.0
b = 0

N = 100 #number of players
R = 100
ps = numpy.linspace(0, 1, 11)
costs = numpy.zeros((R, len(ps)))
for r in range(R):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        tax = [lambda x : 0, lambda x : 0, lambda x : 0]

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[r, pi] = totalc

plt.boxplot(numpy.array(costs) / 0.75)
plt.xticks(numpy.arange(len(ps)) + 1, ['{:0.2f}'.format(p) for p in ps])
plt.xlabel('Parameter p of distribution')
plt.ylabel('Cost of Anarchy with no tax')
plt.ylim(1.0, 4.0 / 3.0)
plt.show()

#%%

N = 100 #number of players
R = 100
ps = numpy.linspace(0, 1, 11)
costs = numpy.zeros((R, len(ps)))
for r in range(R):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        tax = [lambda x : 0, lambda x : x, lambda x : 0]

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[r, pi] = totalc

plt.boxplot(numpy.array(costs) / 0.75)
plt.xticks(numpy.arange(len(ps)) + 1, ['{:0.2f}'.format(p) for p in ps])
plt.xlabel('Parameter p of distribution')
plt.ylabel('Cost of Anarchy with Pigou Tax')
plt.ylim(1.0, 4.0 / 3.0)
plt.show()

#%%
N = 100 #number of players
ts = numpy.linspace(0, 1, 5)
ps = numpy.linspace(0, 1, 10)
costs = numpy.zeros((len(ts), len(ps)))
for ti, t in enumerate(ts):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        tax = [lambda x : 0, lambda x : t, lambda x : 0]

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[ti, pi] = totalc

plt.imshow(numpy.array(costs) / 0.75, interpolation = 'NONE', cmap = plt.cm.Greys, clim = [1.0, 4.0 / 3.0])
plt.colorbar()
plt.xticks(numpy.arange(len(ps)), ['{:0.2f}'.format(p) for p in ps])
plt.yticks(numpy.arange(len(ts)), ['{:0.2f}'.format(t) for t in ts])
plt.xlabel('Parameter p of distribution')
plt.ylabel('Fixed tax value (k)')
plt.title('POA for taxation scheme t = k applied to top road')
#plt.ylim(1.0, 4.0 / 3.0)
plt.show()

#%%
N = 100 #number of players
ts = numpy.linspace(0, 1, 5)
ps = numpy.linspace(0, 1, 10)
costs = numpy.zeros((len(ts), len(ps)))
for ti, t in enumerate(ts):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        tax = [lambda x : 0, lambda x : t * x, lambda x : 0]

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[ti, pi] = totalc

plt.imshow(numpy.array(costs) / 0.75, interpolation = 'NONE', cmap = plt.cm.Greys, clim = [1.0, 4.0 / 3.0])
plt.colorbar()
plt.xticks(numpy.arange(len(ps)), ['{:0.2f}'.format(p) for p in ps])
plt.yticks(numpy.arange(len(ts)), ['{:0.2f}'.format(t) for t in ts])
plt.xlabel('Parameter p of distribution')
plt.ylabel('k')
plt.title('POA for taxation scheme of t = k * x applied to top road')
#plt.ylim(1.0, 4.0 / 3.0)
plt.show()

#%%
N = 100 #number of players
ts = numpy.linspace(0, 2, 10)
ps = numpy.linspace(0, 1, 10)
costs = numpy.zeros((len(ts), len(ps)))
for ti, t in enumerate(ts):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        tax = [lambda x : 0, lambda x : t * (x + x), lambda x : t * 1]

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[ti, pi] = totalc

plt.imshow(numpy.array(costs) / 0.75, interpolation = 'NONE', cmap = plt.cm.Greys, clim = [1.0, 4.0 / 3.0])
plt.colorbar()
plt.xticks(numpy.arange(len(ps)), ['{:0.2f}'.format(p) for p in ps])
plt.yticks(numpy.arange(len(ts)), ['{:0.2f}'.format(t) for t in ts])
plt.xlabel('Parameter p of distribution')
plt.ylabel('k')
plt.title('POA for taxation scheme of k * (c(x) + x * c\'(x))')
#plt.ylim(1.0, 4.0 / 3.0)
plt.show()

#%%
N = 100 #number of players
ts = numpy.linspace(0, 1, 10)
ps = numpy.linspace(0, 1, 10)
costs = numpy.zeros((len(ts), len(ps)))
for ti, t in enumerate(ts):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        if distType == 'bernoulli':
            tax = [lambda x : 0, lambda x : -(a * p + b * (1 - p)) * t, lambda x : 0] #for Bernoulli
        else:
            tax = [lambda x : 0, lambda x : -p * t, lambda x : 0] #for exponential or normal

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[ti, pi] = totalc

plt.imshow(numpy.array(costs) / 0.75, interpolation = 'NONE', cmap = plt.cm.Greys, clim = [1.0, 4.0 / 3.0])
plt.colorbar()
plt.xticks(numpy.arange(len(ps)), ['{:0.2f}'.format(p) for p in ps])
plt.yticks(numpy.arange(len(ts)), ['{:0.2f}'.format(t) for t in ts])
plt.xlabel('Parameter p of distribution')
plt.ylabel('k')
plt.title('POA for taxation scheme t = -k(mean(bias)) applied to top road')
#plt.ylim(1.0, 4.0 / 3.0)
plt.show()

#%%
N = 100 #number of players
ts = numpy.linspace(0, 1, 10)
ps = numpy.linspace(0, 1, 10)
costs = numpy.zeros((len(ts), len(ps)))
for ti, t in enumerate(ts):
    for pi, p in enumerate(ps):
        biases1 = [dist(p) for i in range(N)]

        bias = [lambda i : 0, lambda i : 0, lambda i : biases1[i], lambda i : 0]

        cost = [lambda x : 0, lambda x : x, lambda x : 1.00]
        if distType == 'bernoulli':
            tax = [lambda x : 0, lambda x : -(a * p + b * (1 - p)) * t, lambda x : 0]
        elif distType == 'exponential':
            tax = [lambda x : 0, lambda x : -p**2 * t, lambda x : 0]
        else:
            tax = [lambda x : 0, lambda x : -0.1**2 * t, lambda x : 0]

        start = 0
        end = 3

        totalc, edgeResults, backtrack, converged = game_NE.runRound(edges, start, end, cost, tax, bias, N)
        if not converged:
            raise Exception("Equilibrium didn't converge")
        costs[ti, pi] = totalc

plt.imshow(numpy.array(costs) / 0.75, interpolation = 'NONE', cmap = plt.cm.Greys, clim = [1.0, 4.0 / 3.0])
plt.colorbar()
plt.xticks(numpy.arange(len(ps)), ['{:0.2f}'.format(p) for p in ps])
plt.yticks(numpy.arange(len(ts)), ['{:0.2f}'.format(t) for t in ts])
plt.xlabel('Parameter p of distribution')
plt.ylabel('k')
plt.title('POA for taxation scheme t = -k(var(bias)) applied to top road')
#plt.ylim(1.0, 4.0 / 3.0)
plt.show()

import igraph as ig
from collections import defaultdict
from api import file

def get_adj():
	result = defaultdict(set)
	for l in file.lines('2024/23'):
		a, b = l.split('-')
		result[a].add(b)
		result[b].add(a)
	return result

def test_first():
	adj = get_adj()
	result = sum(
		any(e.startswith('t') for e in [a, b, c])
		for a in adj
		for b in adj[a] if b > a
		for c in adj[a] & adj[b] if c > b
	)
	assert 1064 == result

def test_second():
	adj = get_adj()
	g = ig.Graph()
	for v in adj:
		g.add_vertex(v)
	for v in adj:
		for n in adj[v]:
			if n > v:
				g.add_edge(n, v)
	clique = [g.vs['name'][i] for i in g.largest_cliques()[0]]
	assert 'aq,cc,ea,gc,jo,od,pa,rg,rv,ub,ul,vr,yy' == ','.join(sorted(clique))

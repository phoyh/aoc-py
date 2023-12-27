import math
import itertools as it
import igraph as ig
import networkx as nx
from api import file, parse, RSet

def get_adj():
	return RSet({k: set(vals) for k, *vals in file.lines('2023/25', parse.words)})

def test_first_igraph():
	# type annotations missing everywhere, especially for return types
	gp: ig.Graph = ig.Graph.ListDict(get_adj().to_dictlist())
	c: ig.Cut = gp.mincut()
	assert 598120 == math.prod(sg.vcount() for sg in c.subgraphs())

def test_first_networkx():
	adj = get_adj()
	gp = nx.Graph(adj.to_tuplelist())
	nx.set_edge_attributes(gp, 1, 'capacity')
	pair_it = it.combinations(adj.vertices(), 2)
	cut_size = 0
	sgs = []
	while cut_size != 3:
		start, end = next(pair_it)
		cut_size, sgs = nx.minimum_cut(gp, start, end)
	assert 598120 == math.prod(len(sg) for sg in sgs)

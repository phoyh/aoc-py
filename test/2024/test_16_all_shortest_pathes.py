import networkx as nx
from api import file, graph, PDict, P
N, S, W, E = NSWE = P.NSWE()

def get_input():
	g = PDict.from_lines(file.lines('2024/16_ex'))
	s = max(g.by_value('S'))
	e = max(g.by_value('E'))
	walls = g.by_value('#')
	return g, s, e, walls

def get_neighbors(t, walls):
	p, cur_d = t
	res = {(p, cur_d.rotate_left()), (p, cur_d.rotate_right())}
	if p + cur_d not in walls:
		res.add((p + cur_d, cur_d))
	return res

def get_costs(t1, t2):
	p1, _ = t1
	p2, _ = t2
	return 1000 if p1 == p2 else 1

def input_to_graph(grid, end, walls):
	g = nx.DiGraph()
	end_node = 'end'
	for p in grid - walls:
		for d in NSWE:
			for n in get_neighbors((p, d), walls):
				g.add_edge((p, d), n)
			if p == end:
				g.add_edge((p, d), end_node)
	return g, end_node

def test_first():
	_, start, end, walls = get_input()
	cost, _ = graph.dijkstra(
		(start, E), lambda t: t[0] == end,
		lambda t: get_neighbors(t, walls),
		get_costs
	)
	assert 11048 == cost

def test_second():
	grid, start, end, walls = get_input()
	g, end_node = input_to_graph(grid, end, walls)
	paths = nx.all_shortest_paths(
		g, (start, E), end_node,
		weight=lambda fro, to, _: 0 if to == end_node else get_costs(fro, to)
	)
	assert 64 == len({p for path in paths for p, _ in path[:-1]})

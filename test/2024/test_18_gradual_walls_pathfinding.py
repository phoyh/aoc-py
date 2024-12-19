from collections import deque
import math
from api import file, parse, PSet, P, graph

def get_wall_seq():
	lines = file.lines('2024/18_ex', parse.ints)
	return [P((x, y)) for x, y in lines]

def get_end():
	return P((6, 6))
	#return P((70, 70))

def get_simulation_len():
	return 12
	#return 1024

def get_coords_start_end():
	end = get_end()
	cs = PSet.from_size([e + 1 for e in end])
	return cs, P((0, 0)), end

def get_neighbors_fn(coords):
	return lambda p: p.neighbors(within=coords)

def get_first_blocking_wall(wall_seq, coords, start, end):
	last_waypoints = coords
	cs = {*coords}
	wall_deq = deque(wall_seq)
	while wall_deq:
		w = wall_deq.popleft()
		cs.remove(w)
		if w in last_waypoints:
			cost, path = graph.dijkstra(start, end, get_neighbors_fn(cs))
			last_waypoints = set(path)
			if cost == math.inf:
				return w
	assert False

def test_first():
	wall_seq = get_wall_seq()
	cs, start, end = get_coords_start_end()
	cs_wo_walls = cs - wall_seq[:get_simulation_len()]
	cost, _ = graph.dijkstra(start, end, get_neighbors_fn(cs_wo_walls))
	assert 22 == cost

def test_second():
	wall_seq = get_wall_seq()
	cs, start, end = get_coords_start_end()
	bx, by = get_first_blocking_wall(wall_seq, cs, start, end)
	assert '6,1' == f'{bx},{by}'

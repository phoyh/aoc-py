import itertools as it
import functools as ft
from api import file, graph, P, PDict

@ft.cache
def get_neighbors_w_action(layout, key) -> set[tuple[str, str]]:
	g = PDict.from_lines(layout.split('\n'))
	return {
		k: {
			(g[np], a)
			for a in '^v<>'
			for np in [p + P.by_dir(a)] if np in g and g[np] != ' '
		}
		for p, k in g.items()
	}[key]

def inner_outer_key_neighbors(current: tuple[str, str], layout: str) -> set[tuple[str, str]]:
	inner_key, _ = current
	return {
		(inner_key, 'A'), # pressing A on lower level is always an option
		*get_neighbors_w_action(layout, inner_key) # options for navigating the inner pad
	}

@ft.cache
def get_movements_costs(fro, to, depth, total_depth) -> int:
	if depth == 0:
		# human (= outmost level) can instantly move anywhere
		return 1
	if fro == to:
		# everything's already in place -> just press A
		return 1
	outer_level_start_end = str('A') # outer level's last action must have been A, also end there
	layout = '789\n456\n123\n 0A' if depth == total_depth else ' ^A\n<v>'
	costs, _ = graph.dijkstra(
		(fro, outer_level_start_end),
		(to, outer_level_start_end),
		lambda v: inner_outer_key_neighbors(v, layout),
		edge_cost=lambda a, b: get_movements_costs(a[1], b[1], depth - 1, total_depth)
	)
	return int(costs)

def get_complexity(keypad_depth: int, target: str) -> int:
	total_depth = keypad_depth + 1 # plus one numpad
	return int(target[:-1]) * sum(
		get_movements_costs(fro, to, total_depth, total_depth)
		for fro, to in it.pairwise('A' + target) # start position is always A
	)

def get_complexity_sum(keypad_depth: int) -> int:
	return sum(get_complexity(keypad_depth,target) for target in file.lines('2024/21'))

def test_first():
	assert 231564 == get_complexity_sum(2)

def test_second():
	assert 281212077733592 == get_complexity_sum(25)

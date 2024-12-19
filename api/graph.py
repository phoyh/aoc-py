import heapq
import math
from typing import Callable, TypeVar
import itertools as it
from collections import defaultdict

Vertix = TypeVar('Vertix')

# DIJKSTRA

# Costs are measured by ints, unless the edge cost function returns floats.
# Also, unreachable vertices have costs of math.inf (float).

def __dijkstra_start_todos(start: Vertix | set[Vertix]) \
		-> list[tuple[int | float, Vertix, list[Vertix]]]:
	if not isinstance(start, set):
		start = {start}
	return [(0, s, [s]) for s in start]

def dijkstra(start: Vertix | set[Vertix],
		end: Vertix | Callable[[Vertix], bool],
		neighbors: Callable[[Vertix], set[Vertix]],
		edge_cost: Callable[[Vertix, Vertix], int | float] = lambda *_: 1,
		is_path_prefix_legit: Callable[[list[Vertix]], bool] = lambda *_: True) \
		-> tuple[int | float, list[Vertix]]:
	end_fn = end if callable(end) else lambda v: v == end
	todos = __dijkstra_start_todos(start)
	seen = set()
	while todos:
		cost, vertix, path = heapq.heappop(todos)
		if end_fn(vertix):
			return (cost, path)
		if vertix not in seen and is_path_prefix_legit(path):
			seen.add(vertix)
			for neighborVertix in neighbors(vertix):
				heapq.heappush(todos, (
					cost + edge_cost(vertix, neighborVertix),
					neighborVertix,
					[*path, neighborVertix]
				))
	return (math.inf, [])

def dijkstra_to_all(start: Vertix | set[Vertix],
		neighbors: Callable[[Vertix], set[Vertix]],
		edge_cost: Callable[[Vertix, Vertix], int | float] = lambda *_: 1,
		is_path_prefix_legit: Callable[[list[Vertix]], bool] = lambda *_: True,
		max_costs: float = math.inf) \
		-> dict[Vertix, tuple[int | float, list[Vertix]]]:
	todos = __dijkstra_start_todos(start)
	seen = set()
	result = defaultdict(lambda: (math.inf, []))
	while todos:
		cost, vertix, path = heapq.heappop(todos)
		if vertix not in seen and is_path_prefix_legit(path) and cost <= max_costs:
			result[vertix] = (cost, path)
			seen.add(vertix)
			for neighborVertix in neighbors(vertix):
				heapq.heappush(todos, (
					cost + edge_cost(vertix, neighborVertix),
					neighborVertix,
					[*path, neighborVertix]
				))
	return result

def dijkstra_all_to_all(vertices: list[Vertix],
			get_neighbors: Callable[[Vertix], set[Vertix]],
			get_edge_cost: Callable[[Vertix, Vertix], int | float]
		) -> dict[tuple[Vertix, Vertix], tuple[int | float, list[Vertix] | None]]:
	# modified Floyd–Warshall, O(n^3) - scales badly
	vertix_pairs = set(it.product(vertices, repeat=2))
	distance = {(v1, v2): math.inf if v1 != v2 else 0 for v1, v2 in vertix_pairs}
	next_step_on_path = {(v1, v2): v1 if v1 == v2 else None for v1, v2 in vertix_pairs}
	for v1 in vertices:
		for v2 in get_neighbors(v1):
			distance[(v1, v2)] = get_edge_cost(v1, v2)
			next_step_on_path[(v1, v2)] = v2
	for connector in vertices:
		for v1, v2 in vertix_pairs:
			d_by_connector = distance[v1, connector] + distance[connector, v2]
			if distance[v1, v2] > d_by_connector:
				distance[v1, v2] = d_by_connector
				next_step_on_path[(v1, v2)] = next_step_on_path[(v1, connector)]
	path_w_start_end = {}
	for v1, v2 in vertix_pairs:
		path = [v1]
		curr_v = v1
		while curr_v != v2 and curr_v and next_step_on_path[(curr_v, v2)] is not None:
			curr_v = next_step_on_path[(curr_v, v2)]
			path += [curr_v]
		if curr_v == v2:
			path_w_start_end[(v1, v2)] = path if curr_v == v2 else None
	return {(v1, v2): (distance[(v1, v2)], path_w_start_end[(v1, v2)]) for v1, v2 in vertix_pairs}

import functools as ft
import itertools as it
import api.file
import api.graph
import api.parse

def powerset(l):
	if len(l) <= 1:
		return [[], l]
	result = []
	for rest in powerset(l[1:]):
		result += [rest + l[0:1], rest]
	return result

class Valve:
	def __init__(self, input_line):
		ws = input_line.split()
		self.name = ws[1]
		self.flow = api.parse.ints(input_line)[0]
		self.to_valves_str = [v.replace(',', '') for v in ws[9:]]
		self.to_valves = []
		self.distance_by_valve = {}
	
	def resolve_to(self, tunnel_system):
		self.to_valves = [v for v in tunnel_system.valves if v.name in self.to_valves_str]
	
class TunnelSystem:
	def __init__(self, mini=False):
		self.valves = [Valve(l) for l in api.file.lines('2022/16' + ('_mini' if mini else ''))]
		for v in self.valves:
			v.resolve_to(self)
		connections = api.graph.dijkstra_all_to_all(self.valves, lambda v: v.to_valves, lambda *_: 1)
		for (v1, v2), (distance, _) in connections.items():
			v1.distance_by_valve[v2] = distance
		self.relevant_valves = [v for v in self.valves if v.flow > 0]

	def get_valve_flow(self):
		return {v.name: v.flow for v in self.relevant_valves}
	
	def get_relevant_valve_distances(self):
		rel_vals_with_start = self.relevant_valves + [v for v in self.valves if v.name == 'AA']
		return {(v1.name, v2.name): v1.distance_by_valve[v2]
			for v1, v2 in it.product(rel_vals_with_start, repeat=2)}

@ft.cache
def max_flow(minutes_left, open_valves, location='AA', has_elephant_joker=False):
	result = 0
	for next_valve in open_valves:
		next_mins_left = (minutes_left - distances[location, next_valve]) - 1
		if next_mins_left >= 0:
			this_valve_rest_flow = valve_flow[next_valve] * next_mins_left
			remainder_valve_flows = open_valves - {next_valve}
			subsequent_max = max_flow(next_mins_left, remainder_valve_flows, next_valve, has_elephant_joker)
			result = max(result, this_valve_rest_flow + subsequent_max)
	if has_elephant_joker:
		#alternative: give elephant the rest - he'll have full time though
		result = max(result, max_flow(26, open_valves))
	return result

#ts = TunnelSystem()
ts = TunnelSystem(mini=True)
distances = ts.get_relevant_valve_distances()
valve_flow = ts.get_valve_flow()

def test_first():
	open_valves = frozenset(valve_flow)
	#assert 1871 == max_flow(30, open_valves)
	assert 1651 == max_flow(30, open_valves)

def test_second():
	open_valves = frozenset(valve_flow)
	#assert 2416 == max_flow(26, open_valves, has_elephant_joker=True)
	assert 1707 == max_flow(26, open_valves, has_elephant_joker=True)

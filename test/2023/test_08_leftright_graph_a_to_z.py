import math
import re

import api.file

# Does not work in general but only on the input.
# Reason:
#	steps(Ai->Zi) == steps(Zi->Zi) for each i in 1<=i<=6
#	so no offsets and irregularities need to be considered

def get_required_steps(node, graph, is_right_instr, is_end):
	steps = 0
	while not is_end(node):
		node = graph[node][is_right_instr[steps % len(is_right_instr)]]
		steps += 1
	return steps

def get_least_common_steps(is_start, is_end):
	segs = api.file.segments('2023/08')
	is_right_instr = [i == 'R' for i in segs[0][0]]
	graph = {k: val for k, *val in [re.findall(r'\w+', l) for l in segs[1]]}
	cycles = [
		get_required_steps(n, graph, is_right_instr, is_end)
		for n in graph if is_start(n)
	]
	return math.lcm(*cycles)

def test_first():
	assert 19783 == get_least_common_steps(lambda n: n == 'AAA', lambda n: n == 'ZZZ')

def test_second():
	assert 9177460370549 == get_least_common_steps(
		lambda n: n.endswith('A'), lambda n: n.endswith('Z'))

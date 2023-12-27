import api.file
import math

input = api.file.lines('2019/03')

def getWires():
	result = []
	for wireDef in api.file.lines('2019/03'):
		steps = 0
		p = 0
		pointSteps = {}
		for order in wireDef.split(','):
			v = [1, -1, -1j, 1j]['RLUD'.index(order[0])]
			for _ in range(int(order[1:])):
				steps += 1
				p += v
				pointSteps[p] = steps
		result.append(pointSteps)
	return result

def getIntersections(wires):
	return [(p, [w[p] for w in wires]) for p in wires[0].keys() & wires[1].keys()]	

def test_first():
	assert 1017 == min(abs(p.real) + abs(p.imag) for p, _ in getIntersections(getWires()))

def test_second():
	assert 11432 == min(sum(s) for _, s in getIntersections(getWires()))

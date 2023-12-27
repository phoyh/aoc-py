import numpy as np

def get_pos():
	with open('../aocPython/input/2021/07.txt', 'r') as f:
		return [int(e.strip()) for e in f.readlines()[0].split(',')]

def cost(delta):
	return abs(delta) * (abs(delta) + 1) / 2

def get_accumulative_cost(pos, candidate):
	return sum([cost(p - candidate) for p in pos])

def test_first():
	pos = get_pos()
	med = np.median(pos)
	min_cost = sum(abs(p - med) for p in pos)
	assert 344605 == min_cost

def test_second():
	pos = get_pos()
	mean = round(sum(pos) / len(pos))
	min_cost = min(get_accumulative_cost(pos, i) for i in range(mean - 1, mean + 2))
	assert 93699985 == min_cost

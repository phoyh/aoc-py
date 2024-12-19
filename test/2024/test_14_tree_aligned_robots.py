import math
from collections import defaultdict
from api import P, PSet, file, parse

def get_robots():
	lines = file.lines('2024/14', parse.ints)
	return tuple(zip(*[(P((x, y)), P((vx, vy))) for x, y, vx, vy in lines]))

def get_size():
	return P((101, 103))

def get_mid():
	return get_size() // 2

def tick(rob_pos, rob_vel, tick_num=1):
	return [(rp + rv * tick_num) % get_size() for rp, rv in zip(rob_pos, rob_vel)]

def get_quadrant_score(rob_pos):
	mid = get_mid()
	quads = defaultdict(int)
	for rp in rob_pos:
		s = (rp - mid).sgn()
		if all(se != 0 for se in s):
			quads[s] += 1
	return math.prod(quads.values())

def is_tree(rob_pos):
	pos_set = PSet(rob_pos)
	count_of_robots_with_two_neighbors = sum(
		2 <= sum(n in pos_set for n in p.neighbors())
		for p in rob_pos
	)
	return count_of_robots_with_two_neighbors > len(rob_pos) // 2

def test_first():
	rob_pos, rob_vel = get_robots()
	rob_pos = tick(rob_pos, rob_vel, tick_num=100)
	assert 228457125 == get_quadrant_score(rob_pos)

#def test_second():
def do_not_execute_test_second():
	rob_pos, rob_vel = get_robots()
	steps = 0
	while not is_tree(rob_pos):
		rob_pos = tick(rob_pos, rob_vel)
		steps += 1
	PSet(rob_pos).to_png(f'2024-14-robots_{steps:04d}')
	assert 6493 == steps
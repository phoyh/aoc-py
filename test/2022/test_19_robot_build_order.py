import math
from api import file, parse, P

def get_blueprints_with_id():
	return [
		(id, (
			(P((0, 0, 0, oo)), P((0, 0, 0, 1))),
			(P((0, 0, 0, co)), P((0, 0, 1, 0))),
			(P((0, 0, bc, bo)), P((0, 1, 0, 0))),
			(P((0, gb, 0, go)), P((1, 0, 0, 0))),
			(P((0, 0, 0, 0)), P((0, 0, 0, 0))),
		))
		for id, oo, co, bo, bc, go, gb in file.lines('2022/19_ex', parse.ints)
	]

def get_max_geodes(ticks, blueprint):
	todo = [(P((0, 0, 0, 0)), P((0, 0, 0, 1)))]
	for _ in range(ticks, 0, -1):
		next_todo = []
		for have, make in todo:
			for prod_in, prod_out in blueprint:
				if all(e >= 0 for e in have - prod_in):
					next_todo.append((have + make - prod_in, make + prod_out))
		todo = sorted(next_todo, key = lambda hm: (hm[0] + hm[1], hm[1]))[-100:]
	return max(have[0] for have, _ in todo)

def test_first():
	blueprints_with_id = get_blueprints_with_id()
	assert 33 == sum(
		id * get_max_geodes(24, blueprint) for id, blueprint in blueprints_with_id
	)

def test_second():
	blueprints_with_id = get_blueprints_with_id()
	assert 2604 == math.prod(
		get_max_geodes(32, blueprint) for _, blueprint in blueprints_with_id[:3]
	)

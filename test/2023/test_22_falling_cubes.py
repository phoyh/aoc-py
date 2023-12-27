from collections import defaultdict
import itertools as it

from api import file, parse, RSet, xmath

def get_belows(cubes) -> RSet:
	result = RSet() # no vertices set, all cubes have at least one limitation
	zc_by_xy = defaultdict(list)
	for cidx, (ax, ay, az, bx, by, _) in enumerate(cubes):
		for x in range(ax, bx + 1):
			for y in range(ay, by + 1):
				zc_by_xy[x, y].append((az, cidx))
	for el in zc_by_xy.values():
		el.sort()
		for (_, below), (_, above) in it.pairwise(el):
			result[above].add(below)
	return result

def get_stands_on(falling_cubes, belows: RSet):
	cidx_order = belows.topologic_order(is_predecessors_by=True)
	upper_z_by_standing_cube = {}
	stands_on = RSet()
	for cidx in cidx_order:
		_, _, az, _, _, bz = falling_cubes[cidx]
		stands_on_idxs, z_below = xmath.argmax_max(belows[cidx], lambda ci: upper_z_by_standing_cube[ci])
		stands_on[cidx] = set(stands_on_idxs)
		my_z = 1 + z_below
		upper_z_by_standing_cube[cidx] = my_z + bz - az
	return stands_on

def test_first():
	falling_cubes = file.lines('2023/22', parse.ints)
	belows = get_belows(falling_cubes)
	stands_on = get_stands_on(falling_cubes, belows)
	supports = stands_on.reverse()
	assert 416 == sum(
		all(len(stands_on[si]) > 1 for si in supported_idxs)
		for supported_idxs in supports.values()
	)

def test_second():
	falling_cubes = file.lines('2023/22', parse.ints)
	belows = get_belows(falling_cubes)
	stands_on = get_stands_on(falling_cubes, belows)
	supports = stands_on.reverse()
	result = 0
	for cidx in range(len(falling_cubes)):
		todo = list(supports[cidx])
		fallers = {cidx}
		while todo:
			fi = todo.pop()
			if fi not in fallers and not stands_on[fi] - fallers:
				fallers.add(fi)
				todo.extend(supports[fi])
		result += len(fallers) - 1
	assert 60963 == result

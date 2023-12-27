from api.cube import Cube, CubeSet
import api.file
import api.parse

def range_to_cube(r_from, r_to):
	return Cube([(r_from, r_from + r_to - 1)])

def do_step(range_cubesets, maps: list[tuple[int, Cube]]):
	res_cs = range_cubesets - CubeSet([c for _, c in maps])
	for range_c in range_cubesets.get_cubes():
		res_cs = res_cs | CubeSet([
			intersect_c.move([m_dest_from - m_c.min()[0]])
			for m_dest_from, m_c in maps
			if len(intersect_c := range_c & m_c)
		])
	return res_cs

def solve(seed_nums_to_ranges):
	seed_seg, *step_segs = api.file.segments('2023/05', api.parse.uints)
	seed_ranges = seed_nums_to_ranges(seed_seg[0])
	range_cubesets = CubeSet([range_to_cube(*r) for r in seed_ranges])
	for s in step_segs:
		maps = [
			(m_dest_from, range_to_cube(m_from, m_len))
			for m_dest_from, m_from, m_len in s[1:]
		]
		range_cubesets = do_step(range_cubesets, maps)
	return min(c.min()[0] for c in range_cubesets.get_cubes())

def test_first():
	assert 227653707 == solve(lambda seeds: [(s, 1) for s in seeds])

def test_second():
	assert 78775051 == solve(lambda seeds: zip(seeds[::2], seeds[1::2]))
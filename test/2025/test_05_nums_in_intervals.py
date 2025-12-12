from api import Cube, CubeSet, file, parse

def get_cubeset_and_numbers():
	ranges, nums_str = file.segments('2025/05_ex')
	cs = CubeSet()
	for r in ranges:
		f, t = parse.uints(r)
		cs |= Cube([(f, t)])
	return cs, list(map(int, nums_str))

def test_first():
	cs, nums = get_cubeset_and_numbers()
	assert 3 == sum((n,) in cs for n in nums)

def test_second():
	cs, _ = get_cubeset_and_numbers()
	assert 14 == len(cs)

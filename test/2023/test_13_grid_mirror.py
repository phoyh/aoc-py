from api import PDict, file

def mirror(y, mirror_y_plus_point_five):
	return 2 * mirror_y_plus_point_five - 1 - y

def get_horizontal_reflection(hashes, off_by):
	_, height = hashes.size_by_dim()
	for my in range(1, height):
		mirrored_hashes_in_canvas = {(x, mirror(y, my)) for x, y in hashes if 0 <= mirror(y, my) < height}
		if len(mirrored_hashes_in_canvas - hashes) == off_by:
			return my
	return 0

def solve(off_by):
	hashes_list = [PDict.from_lines(s).by_value('#') for s in file.segments('2023/13')]
	return sum(
		f * get_horizontal_reflection(h, off_by)
		for hashes in hashes_list
		for f, h in [(100, hashes), (1, hashes.transpose())]
	)

def test_first():
	assert 33520 == solve(0)

def test_second():
	assert 34824 == solve(1)
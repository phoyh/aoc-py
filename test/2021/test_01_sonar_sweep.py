import api.file

def get_increases(package_size):
	measurements = api.file.lines('2021/01', int)
	comparision_points = zip(measurements, measurements[package_size:])
	return sum([b > a for a, b in comparision_points])

def test_first():
	assert 1482 == get_increases(1)

def test_second():
	assert 1518 == get_increases(3)

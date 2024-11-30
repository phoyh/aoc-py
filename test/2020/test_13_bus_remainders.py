from api import xmath, file

def get_input():
	lines = file.lines('2020/13')
	bus_idx_w_periods = [(i, int(p)) for i, p in enumerate(lines[1].split(',')) if p != 'x']
	return int(lines[0]), bus_idx_w_periods, [p for _, p in bus_idx_w_periods]

def get_wait_time(time, bus_period):
	return (bus_period - time % bus_period) % bus_period

def test_first():
	earliest, _, bus_periods = get_input()
	mins, min_value = xmath.argmin_min(bus_periods, lambda p: get_wait_time(earliest, p))
	assert 2095 == mins[0] * min_value

def test_second():
	_, bus_idx_w_periods, bus_periods = get_input()
	remainders = [get_wait_time(dt, p) for dt, p in bus_idx_w_periods]
	assert 598411311431841 == xmath.chinese_remainder(remainders, bus_periods)

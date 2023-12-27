import math
import z3

from api import file, search, z3result

def get_split_lines():
	return [l.split()[1:] for l in file.lines('2023/06')]

def get_highscore_num(race_time, highscore_dist):
	def dist_over_hs(button_time):
		return (race_time - button_time) * button_time - highscore_dist
	first_inclusive = search.sign_change(0, race_time // 2, dist_over_hs)
	second_exclusive = search.sign_change(race_time // 2, race_time, dist_over_hs)
	return second_exclusive - first_inclusive

def test_first():
	times, distances = [map(int, ins) for ins in get_split_lines()]
	assert 1413720 == math.prod([
		get_highscore_num(time, dist)
		for time, dist in zip(times, distances)
	])

def test_second():
	time, dist = [int(''.join(l)) for l in get_split_lines()]
	assert 30565288 == get_highscore_num(time, dist)

############

def test_first_z3():
	time, dist = map(int, [l[0] for l in get_split_lines()])
	s = z3.Solver()
	time_held_z3 = z3.Int('t')
	distance_z3 = z3.Int('d')
	distance_m1_z3 = z3.Int('dm1')
	s.add(distance_z3 == (time - time_held_z3) * time_held_z3)
	s.add(distance_m1_z3 == (time - (time_held_z3 - 1)) * (time_held_z3 - 1))
	s.add(z3.Or(
		z3.And(distance_z3 > dist, distance_m1_z3 <= dist),
		z3.And(distance_z3 <= dist, distance_m1_z3 > dist)
	))
	sol1, sol2 = sorted(z3result.all_ints(s, time_held_z3))
	highscore_num = sol2 - sol1
	assert 30 == highscore_num

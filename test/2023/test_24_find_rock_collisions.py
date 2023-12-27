import itertools as it
import numpy as np
import z3

from api import file, parse, z3result

def test_first_numpy():
	hs = file.lines('2023/24', parse.ints)
	res = 0
	mi, ma = 200000000000000, 400000000000000
	for (x1, y1, _, vx1, vy1, _), (x2, y2, _, vx2, vy2, _) in it.combinations(hs, 2):
		m = np.array([[vx1, -vx2], [vy1, -vy2]])
		r = np.array([x2 - x1, y2 - y1])
		try:
			t1, t2 = np.linalg.solve(m, r)
			if t1 > 0 and t2 > 0 and all(mi <= c + t1 * vc <= ma for c, vc in [(x1, vx1), (y1, vy1)]):
				res += 1
		except np.linalg.LinAlgError:
			pass
	assert 27328 == res

def test_first_z3():
	hs = file.lines('2023/24_ex', parse.ints)
	res = 0
	mi, ma = 7, 27
	for (x1, y1, _, vx1, vy1, _), (x2, y2, _, vx2, vy2, _) in it.combinations(hs, 2):
		s = z3.Solver()
		t1, t2, cx, cy = (z3.Real(n) for n in 't1,t2,cx,cy'.split(','))
		s.add(t1 > 0)
		s.add(t2 > 0)
		for c, s1, v1, s2, v2 in (cx, x1, vx1, x2, vx2), (cy, y1, vy1, y2, vy2):
			s.add(c > mi)
			s.add(c < ma)
			s.add(c == s1 + v1 * t1)
			s.add(c == s2 + v2 * t2)
		if s.check() == z3.sat:
			res += 1
	assert 2 == res

def test_second_int():
	hs = file.lines('2023/24_ex', parse.ints)
	s = z3.Solver()
	rx, ry, rz, rvx, rvy, rvz = (z3.Int('r' + n) for n in 'x,y,z,vx,vy,vz'.split(','))
	for idx, (hx, hy, hz, hvx, hvy, hvz) in enumerate(hs):
		t = z3.Int(f't{idx}')
		s.add(t > 0)
		for hs, hv, rs, rv in [(hx, hvx, rx, rvx), (hy, hvy, ry, rvy), (hz, hvz, rz, rvz)]:
			s.add(hs + hv * t == rs + rv * t)
	res = z3result.next_int_tuple(s, (rx, ry, rz))
	assert res is not None
	assert 47 == sum(res)

def test_second_real():
	hs = file.lines('2023/24', parse.ints)
	s = z3.Solver()
	rx, ry, rz, rvx, rvy, rvz = (z3.Real('r' + n) for n in 'x,y,z,vx,vy,vz'.split(','))
	for idx, (hx, hy, hz, hvx, hvy, hvz) in enumerate(hs):
		t = z3.Real(f't{idx}')
		s.add(t > 0)
		for hs, hv, rs, rv in [(hx, hvx, rx, rvx), (hy, hvy, ry, rvy), (hz, hvz, rz, rvz)]:
			s.add(hs + hv * t == rs + rv * t)
	res = z3result.next_int_tuple(s, (rx, ry, rz))
	assert res is not None
	assert 722976491652740 == sum(res)

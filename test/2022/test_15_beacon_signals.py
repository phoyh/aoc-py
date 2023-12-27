# pyright: reportGeneralTypeIssues=false, reportOptionalMemberAccess=false
# pylint: disable=no-member
import z3

from api import Cube, CubeSet, file, parse, z3result

def get_readings(filename):
	result = []
	for l in file.lines(filename):
		sx, sy, bx, by = parse.ints(l)
		dist = abs(sx - bx) + abs(sy - by)
		result += [(sx, sy, bx, by, dist)]
	return result

def cube_can_contain_solution(data, cube):
	min_x, min_y = cube.min()
	max_x, max_y = cube.max()
	for sx, sy, *_, dist in data:
		if all(abs(x - sx) + abs(y - sy) <= dist for x in [min_x, max_x] for y in [min_y, max_y]):
			return False
	return True

def test_first():
	pivot_y = 10
	intervals_on_pivot = CubeSet([])
	beakons_on_pivot = set()
	for sx, sy, bx, by, dist in get_readings('2022/15_mini'):
		if by == pivot_y:
			beakons_on_pivot.add(bx)
		x_budget = dist - abs(sy - pivot_y)
		if x_budget >= 0:
			new_interval = Cube([(sx - x_budget, sx + x_budget)])
			intervals_on_pivot = intervals_on_pivot | new_interval
	result = len(intervals_on_pivot) - len(beakons_on_pivot)
	assert 26 == result

def test_second_binary_search():
	margin_max = 4_000_000
	data = get_readings('2022/15')
	todo = [Cube([(0, margin_max)] * 2)]
	solution = None
	while solution is None:
		c = todo.pop()
		if cube_can_contain_solution(data, c):
			if len(c) == 1:
				solution = c
			else:
				todo += c.quadrants()
	x, y = solution.min()
	result = margin_max * x + y
	assert 12555527364986 == result 

def test_second_z3():
	margin_max = 4_000_000
	s = z3.Solver()
	solver_x = z3.Int('x')
	solver_y = z3.Int('y')
	solver_vars = (solver_x, solver_y)
	for se in solver_vars:
		s.add(0 <= se)
		s.add(se <= margin_max)
	z3_abs = lambda e: z3.If(e >= 0, e, -e)
	for sx, sy, *_, dist in get_readings('2022/15'):
		s.add(z3_abs(solver_x - sx) + z3_abs(solver_y - sy) > dist)
	x, y = z3result.next_int_tuple(s, solver_vars)
	result = margin_max * x + y
	assert 12555527364986 == result 

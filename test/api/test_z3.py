import z3
from api import z3result

def test_many_solutions():
	s = z3.Solver()
	x = z3.Int('x')
	s.add(x < 10)
	s.add(x > 0)
	s.add(z3.Or(
		x % 2 == 0,
		x < 5
	))
	relu = lambda e: z3.If(e >= 0, e, 0)
	s.add(relu(x - 6) == 0)
	assert {1, 2, 3, 4, 6} == z3result.all_ints(s, x)

def test_one_solution_multivar():
	s = z3.Solver()
	x = z3.Int('x')
	y = z3.Int('y')
	s.add(x % y == 2)
	s.add(x > 2)
	s.add(x < 7)
	s.add(z3.Or(y == 3, y == 2))
	assert (5, 3) == z3result.next_int_tuple(s, (x, y))
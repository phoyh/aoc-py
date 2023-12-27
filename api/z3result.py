import z3

def all_int_tuples(s: z3.Solver, int_variables: tuple[z3.ArithRef, ...]) \
		-> set[tuple[int]]:
	"""
	Each solution vector of the result set has the same ordering as int_variables.

	Note the side effect on the solver by squeezing out all solutions.
	"""
	result = set()
	while (solution_vector := next_int_tuple(s, int_variables)):
		result.add(solution_vector)
	return result

def all_ints(s: z3.Solver, int_variable: z3.ArithRef) \
		-> set[int]:
	return {x for x, *_ in all_int_tuples(s, (int_variable,))}

def next_int_tuple(s: z3.Solver, int_variables: tuple[z3.ArithRef, ...]) \
		-> tuple[int, ...] | None:
	"""
	Result vector has the same ordering as int_variables.

	Note the side effect on the solver by squeezing out the returned solution.
	"""
	if s.check() != z3.sat:
		return None
	solution_vector = []
	new_conditions = []
	for var in int_variables:
		solution = s.model()[var].as_long() # type: ignore pylint: disable=no-member
		solution_vector.append(solution)
		new_conditions.append(var != solution)
	if len(new_conditions) == 1:
		s.add(new_conditions[0])
	else:
		s.add(z3.Or(*new_conditions))
	return tuple(solution_vector)

def next_int(s: z3.Solver, int_variable: z3.ArithRef) \
		-> int | None:
	t = next_int_tuple(s, (int_variable,))
	return t[0] if t else None

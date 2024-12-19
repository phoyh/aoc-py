import z3

def get_model_var_value(model: z3.ModelRef, int_var: z3.ExprRef) -> int:
	return model[int_var].as_long() # type: ignore pylint: disable=no-member

########## Solver ##########

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
		solution = get_model_var_value(s.model(), var)
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

######## OPTIMIZER ########

def minimize(o: z3.Optimize, int_var_to_be_min: z3.ArithRef) -> int | None:
	"""
	Minimize the int_variable and return the minimized value.
	"""
	o.minimize(int_var_to_be_min)
	if o.check() != z3.sat:
		return
	return get_model_var_value(o.model(), int_var_to_be_min)

def minimize_and_get_vars(o: z3.Optimize, int_var_to_be_min: z3.ArithRef,
		model_vars_of_interest: list[z3.ArithRef]) -> tuple[int, list[int]] | None:
	"""
	Minimize the int_variable and return the minimized value
	together with the values of any model variables of interest.
	"""
	o.minimize(int_var_to_be_min)
	if o.check() != z3.sat:
		return
	m = o.model()
	return (get_model_var_value(m, int_var_to_be_min),
		[get_model_var_value(m, mv) for mv in model_vars_of_interest])

def maximize(o: z3.Optimize, int_var_to_be_max: z3.ArithRef) -> int | None:
	"""
	Maximize the int_variable and return the maximized value.
	"""
	o.maximize(int_var_to_be_max)
	if o.check() != z3.sat:
		return
	return get_model_var_value(o.model(), int_var_to_be_max)

def maximize_and_get_vars(o: z3.Optimize, int_var_to_be_max: z3.ArithRef,
		model_vars_of_interest: list[z3.ArithRef]) -> tuple[int, list[int]] | None:
	"""
	Maximize the int_variable and return the maximized value
	together with the values of any model variables of interest.
	"""
	o.maximize(int_var_to_be_max)
	if o.check() != z3.sat:
		return
	m = o.model()
	return (get_model_var_value(m, int_var_to_be_max),
		[get_model_var_value(m, mv) for mv in model_vars_of_interest])

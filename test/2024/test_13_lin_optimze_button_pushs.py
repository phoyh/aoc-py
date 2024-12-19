import z3
from api import file, parse, z3result

def get_machines(suffix: str = '', target_add_on: int = 0):
	return [
		(a, b, [te + target_add_on for te in t])
   		for a, b, t in file.segments(f'2024/13{suffix}', parse.ints)
	]

def get_cost(button_a, button_b, target):
	a_x, a_y = button_a
	b_x, b_y = button_b
	t_x, t_y = target
	b_nom = t_x * a_y - t_y * a_x
	b_denom = b_x * a_y - b_y * a_x
	if b_denom != 0 and b_nom % b_denom == 0:
		b = b_nom // b_denom
		a = (t_x - b_x * b) // a_x
		return 3 * a + b

def test_first():
	assert 31897 == sum(get_cost(*m) or 0 for m in get_machines())

def test_second():
	assert 87596249540359 == sum(
		get_cost(a, b, t) or 0
		for a, b, t in get_machines(target_add_on=10000000000000)
	)

########### real optimization @ z3 ##############

def get_optimal_cost(button_a: list[int], button_b: list[int],
		target: list[int]) -> int | None:
	o = z3.Optimize()
	a_presses = z3.Int('ap')
	b_presses = z3.Int('bp')
	o.add(a_presses > 0)
	o.add(b_presses > 0)
	cost = z3.Int('c')
	o.add(cost == a_presses * 3 + b_presses)
	for ba, bb, t in zip(button_a, button_b, target):
		o.add(t == ba * a_presses + bb * b_presses)
	return z3result.minimize(o, cost)

def test_first_z3():
	assert 480 == sum(
		get_optimal_cost(*m) or 0
		for m in get_machines(suffix='_ex')
	)

def test_second_z3():
	assert 875318608908 == sum(
		get_optimal_cost(*m) or 0
		for m in get_machines(suffix='_ex', target_add_on=10000000000000)
	)

import operator as op
from api import file, parse

def is_feasible(left, right, operators):
	values = {right[0]}
	for r in right[1:]:
		values = {o(v, r) for o in operators for v in values}
	return left in values

def sum_of_feasible_equations(operators, suffix, fn_is_feasible):
	lines = file.lines(f'2024/07{suffix}', parse.ints)
	return sum(left for left, *right in lines if fn_is_feasible(left, right, operators))

def int_concat(a, b):
	assert min(a, b) >= 0
	return int(str(a) + str(b))

def test_first():
	assert 3749 == sum_of_feasible_equations([op.add, op.mul], '_ex', is_feasible)

def test_second():
	assert 11387 == sum_of_feasible_equations([op.add, op.mul, int_concat], '_ex', is_feasible)

########## right-to-left speedup x100+ ##########

def is_feasible_rtl(left, right, operators):
	values = {left}
	for r in right[-1:0:-1]:
		values = {o(v, r) for o in operators for v in values} - {None}
	return right[0] in values

def reverse_add(res, b) -> int | None:
	if res >= b:
		return res - b

def reverse_mul(res, b) -> int | None:
	if res % b == 0:
		return res // b

def reverse_int_concat(res, b) -> int | None:
	bl = len(str(b))
	rs = str(res)
	if rs[-bl:] == str(b) and len(rs) > bl:
		return int(rs[:-bl])

def test_first_rtl():
	assert 3598800864292 == sum_of_feasible_equations([reverse_add, reverse_mul], '', is_feasible_rtl)

def test_second_rtl():
	assert 340362529351427 == sum_of_feasible_equations(
		[reverse_add, reverse_mul, reverse_int_concat], '', is_feasible_rtl)

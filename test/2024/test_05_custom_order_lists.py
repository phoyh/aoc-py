import itertools as it
import functools as ft

from api import file, parse, RSet

def get_input():
	constraints_list, lists = file.segments('2024/05', parse.ints)
	return RSet.from_list(constraints_list), lists

def is_valid(constraints, l):
	return all(
		a not in constraints[b]
		for a, b in it.pairwise(l)
	)

def sorted_by_constraints(constraints, l):
	return sorted(l, key=ft.cmp_to_key(lambda a, b: -1 if a in constraints[b] else 1))

def test_first():
	constraints, lists = get_input()
	assert 5747 == sum(
		l[len(l) // 2]
		for l in lists
		if is_valid(constraints, l)
	)

def test_second():
	constraints, lists = get_input()
	assert 5502 == sum(
		sorted_by_constraints(constraints, l)[len(l) // 2]
		for l in lists
		if not is_valid(constraints, l)
	)

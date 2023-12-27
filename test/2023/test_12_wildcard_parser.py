import functools as ft
from api import file

def get_row_groups(line, expand_factor):
	row_str, groups_str = line.split()
	row = '?'.join([row_str] * expand_factor) + '.'
	groups = tuple(int(g) for g in groups_str.split(',')) * expand_factor
	return row, groups

@ft.cache
def possible_assignments(row: str, groups: tuple[int, ...], damage_streak = 0):
	if not row:
		return not groups
	todo = set()
	if row[0] in '.?':
		if not damage_streak:
			todo.add((groups, 0))
		else:
			if groups and groups[0] == damage_streak:
				todo.add((groups[1:], 0))
	if row[0] in '#?':
		todo.add((groups, damage_streak + 1))
	return sum(possible_assignments(row[1:], *td) for td in todo)

def solve(expand_factor):
	return sum(
		possible_assignments(*get_row_groups(l, expand_factor))
		for l in file.lines('2023/12_ex')
	)

def test_first():
	assert 21 == solve(1)

def test_second():
	assert 525152 == solve(5)
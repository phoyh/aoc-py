from collections import Counter
import sys
from api import file, P, PDict, PSet

N, S, W, E = NSWE = P.NSWE()
O = P.O()

def get_next(elf: P, elves, step) -> P:
	if all(n not in elves for n in elf.neighbors(diag = True)):
		return elf
	results = [
		d if all(elf + d + e not in elves for e in diag_elems) else None
		for d, diag_elems in zip(NSWE, [[O, W, E], [O, W, E], [O, N, S], [O, N, S]])
	]
	for i in range(4):
		idx = (i + step) % 4
		if results[idx]:
			return elf + results[idx]
	return elf

def solve(max_steps = sys.maxsize):
	grid = PDict.from_lines(file.lines('2022/23_ex'))
	old_elves = PSet()
	elves = grid.by_value('#')
	step = 0
	while elves != old_elves and step < max_steps:
		old_elves = elves
		next_by_elf = {
			elf: get_next(elf, old_elves, step)
			for elf in elves
		}
		counts_by_next = Counter(next_by_elf.values())
		elves = PSet({
			elf if counts_by_next[next_by_elf[elf]] > 1 else next_by_elf[elf]
			for elf in elves
		})
		step += 1
	if step < max_steps:
		return step
	return Counter(PDict.from_points(elves, '#', '.').to_str_2d())['.']

def test_first():
	assert 110 == solve(10)

def test_second():
	assert 20 == solve()

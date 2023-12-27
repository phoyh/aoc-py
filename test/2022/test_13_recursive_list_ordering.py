import functools as ft
import math
import ast
import api.file

def get_pairs():
	return [[ast.literal_eval(l) for l in s] for s in api.file.segments('2022/13')]

def cmp(t1, t2):
	match t1, t2:
		case int(), int():
			return t1 - t2
		case int(), list():
			return cmp([t1], t2)
		case list(), int():
			return cmp(t1, [t2])
		case _:
			for e_cmp in map(cmp, t1, t2):
				if e_cmp:
					return e_cmp
			return len(t1) - len(t2)

def test_first():
	pairs = get_pairs()
	assert 4643 == sum(1 + pi for pi, (t1, t2) in enumerate(pairs) if cmp(t1, t2) <= 0)

def test_second():
	extra = [[[2]], [[6]]]
	packets = extra + [t for p in get_pairs() for t in p]
	packets.sort(key=ft.cmp_to_key(cmp))
	assert 21614 == math.prod(1 + packets.index(e) for e in extra)
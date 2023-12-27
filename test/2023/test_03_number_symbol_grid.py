import re
import math

import api.file

def get_symbols_numbers():
	lines = api.file.lines('2023/03')
	symbols = {
		(x, y): c
		for y, l in enumerate(lines)
		for x, c in enumerate(l)
		if c != '.' and not str.isdigit(c)
	}
	numbers = [
		(int(m.group(0)), [
			(sx, sy) for sx, sy in symbols.keys()
			if m.start() - 1 <= sx <= m.end() and y - 1 <= sy <= y + 1
		])
		for y, l in enumerate(lines)
		for m in re.finditer(r'\d+', l)
	]
	return (symbols, numbers)

def test_first():
	_, numbers = get_symbols_numbers()
	assert 546312 == sum(val for val, syms in numbers if len(syms) > 0)

def test_second():
	symbols, numbers = get_symbols_numbers()
	sym_numbers = [
		[val for val, nsxy in numbers if sxy in nsxy]
		for sxy, s in symbols.items() if s == '*'
	]
	assert 87449461 == sum(math.prod(sns) for sns in sym_numbers if len(sns) == 2)

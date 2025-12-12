import math

from api import file, parse

def get_lines():
	return file.lines('2025/06')

def calc_totals(ops, operands_block):
	return sum(
		{'+': sum, '*': math.prod}[op](operands)
		for op, operands in zip(ops, operands_block)
	)

def test_first():
	lines = get_lines()
	assert 5335495999141 == calc_totals(
		lines[-1].split(),
		zip(*(parse.ints(l) for l in lines[:-1]))
	)

def test_second_B():
	lines = get_lines()
	padded_len = 1 + max(len(l) for l in lines)
	padded_lines = [l.ljust(padded_len) for l in lines]
	operand_by_x = [''.join(cl) for cl in zip(*padded_lines[:-1])]
	operands_blocks = []
	operands = []
	for operand in operand_by_x:
		if operand.strip():
			operands.append(int(operand))
		else:
			operands_blocks.append(operands)
			operands = []
	assert 10142723156431 == calc_totals(lines[-1].split(), operands_blocks)

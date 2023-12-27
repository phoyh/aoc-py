import itertools as it
import numpy as np

def get_lines():
	with open('../aocPython/input/2021/08.txt', 'r') as f:
		return [[side.strip().split(' ') for side in l.split('|')] for l in f.readlines()]

def count_unique(line):
	return sum(len(e) in [2, 3, 4, 7] for e in line)

digits = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
perms = list(it.permutations(list('abcdefg')))

def apply_perm(perm, digit):
	indexes = [ord(e) - 97 for e in list(digit)]
	mapped_digits = [perm[i] for i in indexes]
	return ''.join(sorted(mapped_digits))

def get_perm(input):
	for p in perms:
		if all(apply_perm(p, d) in digits for d in input):
			return p
	assert 0 == 1

def get_value(normalized_digits):
	return int(''.join([str(digits.index(d)) for d in normalized_digits]))

def test_first():
	assert 330 == sum(count_unique(l[1]) for l in get_lines())

def test_second():
	output_sum = 0
	for input, output in get_lines():
		p = get_perm(input)
		output_sum += get_value([apply_perm(p, o) for o in output])
	assert 1010472 == output_sum
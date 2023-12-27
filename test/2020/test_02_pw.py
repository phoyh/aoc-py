import re

import api.file

def line_conv(l):
	grs = re.fullmatch(r'(\d+)-(\d+) (.): (.+)', l)
	assert grs
	val1, val2, letter, pw = grs.groups()
	return (int(val1), int(val2), letter, pw)

def get_input():
	return api.file.lines('2020/02', line_conv)

def test_first():
	result = sum(
		1
		for occ_min, occ_max, letter, pw in get_input()
		if occ_min <= sum(1 for pwl in pw if pwl == letter) <= occ_max
	)
	assert 638 == result

def test_second():
	result = sum(
		1
		for pos1, pos2, letter, pw in get_input()
		if (pw[pos1 - 1] == letter) ^ (pw[pos2 - 1] == letter)
	)
	assert 699 == result
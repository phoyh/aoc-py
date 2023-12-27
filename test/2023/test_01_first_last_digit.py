import re

import api.file

def to_digits(line):
	return re.findall(r'\d', line)

def to_digits_incl_words(line):
	for i, w in enumerate('one, two, three, four, five, six, seven, eight, nine'.split(', ')):
		line = line.replace(w, w + str(i + 1) + w)
	return to_digits(line)

def get_value(digits):
	return int(digits[0] + digits[-1])

def test_first():
	lines = api.file.lines('2023/01', to_digits)
	assert 54877 == sum(get_value(l) for l in lines)

def test_second():
	lines = api.file.lines('2023/01', to_digits_incl_words)
	assert 54100 == sum(get_value(l) for l in lines)
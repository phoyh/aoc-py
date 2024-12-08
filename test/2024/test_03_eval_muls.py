import re
from api import file

def get_input():
	return ' '.join(file.lines('2024/03'))

def eval_muls(text):
	tuples = re.findall(r'mul\((\d+),(\d+)\)', text)
	return sum(int(a) * int(b) for a, b in tuples)

def test_first():
	assert 164730528 == eval_muls(get_input())

def test_second():
	assert 70478672 == eval_muls(re.sub(r'don\'t\(\).*?(do\(\)|$)', ' ', get_input()))

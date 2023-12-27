import re

def ints(line: str) -> list[int]:
	return [int(e) for e in re.findall(r'-?\d+', line)]

def uints(line: str) -> list[int]:
	return [int(e) for e in re.findall(r'\d+', line)]

def words(line: str) -> list[int]:
	return re.findall(r'\w+', line)

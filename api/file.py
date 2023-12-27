from typing import Callable, TypeVar

T = TypeVar('T')

def readall(path_in_input_wo_suffix: str) -> str:
	with open('../aocPython/input/' + path_in_input_wo_suffix + '.txt', 'r') as f:
		return f.read().strip()

def segments(path_in_input_wo_suffix: str,
		line_converter: Callable[[str], T] = lambda l: l) \
		-> list[list[T]]:
	raw_segments = readall(path_in_input_wo_suffix).split('\n\n')
	return [[line_converter(l) for l in sg.splitlines()] for sg in raw_segments]

def lines(path_in_input_wo_suffix, line_converter: Callable[[str], T] = lambda l: l) \
		-> list[T]:
	s = readall(path_in_input_wo_suffix)
	return [line_converter(l) for l in s.splitlines()]
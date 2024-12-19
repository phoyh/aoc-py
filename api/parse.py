import re

def __line_or_lines_to_line(line_or_lines: str | list[str]) -> str:
	if isinstance(line_or_lines, str):
		return line_or_lines
	return '\n'.join(line_or_lines)

def ints(line_or_lines: str | list[str]) -> list[int]:
	line = __line_or_lines_to_line(line_or_lines)
	return [int(e) for e in re.findall(r'-?\d+', line, flags=re.MULTILINE)]

def uints(line_or_lines: str | list[str]) -> list[int]:
	line = __line_or_lines_to_line(line_or_lines)
	return [int(e) for e in re.findall(r'\d+', line, flags=re.MULTILINE)]

def words(line_or_lines: str | list[str]) -> list[int]:
	line = __line_or_lines_to_line(line_or_lines)
	return re.findall(r'\w+', line, flags=re.MULTILINE)

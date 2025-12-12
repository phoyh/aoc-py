from api import file, parse

def is_valid(num: str, max_rep: int | None = None) -> bool:
	return all(
		num != num[:prefix_len] * (min(max_rep or len(num), len(num) // prefix_len))
		for prefix_len in range(1, 1 + len(num) // 2)
	)

def sum_invalid(max_rep: int | None = None) -> int:
	return sum(
		n
		for r in file.readall('2025/02_ex').split(',')
		for a, b in [parse.uints(r)]
		for n in range(a, b + 1)
		if not is_valid(str(n), max_rep)
	)

def test_first():
	assert 1227775554 == sum_invalid(2)

def test_second():
	assert 4174379265 == sum_invalid()

from api import file

def get_sequences():
	return file.lines('2025/03')

def get_max_subsequence(numstr: str, seq_len: int) -> int:
	digits = ''
	for dig_left in range(seq_len, 0, -1):
		max_digit = max(numstr[:len(numstr) - dig_left + 1])
		numstr = numstr[1 + numstr.index(max_digit):]
		digits += max_digit
	return int(digits)

def test_first():
	assert 17278 == sum(get_max_subsequence(s, 2) for s in get_sequences())

def test_second():
	assert 171528556468625 == sum(get_max_subsequence(s, 12) for s in get_sequences())

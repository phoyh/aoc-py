def get_diagnostics():
	with open('input/2021/03.txt', 'r') as f:
		return [[int(e) for e in list(l.strip())] for l in f.readlines()]

def get_most_common(binary_array, binary_index):
	ones = sum(b[binary_index] for b in binary_array)
	return 1 if ones * 2 >= len(binary_array) else 0

def get_gamma(diag):
	return [get_most_common(diag, i) for i in range(len(diag[0]))]

def get_epsilon(diag):
	return [1 - ge for ge in get_gamma(diag)]

def find_line_based_on_commonality(diag, target_by_most_common):
	candidates = diag.copy()
	for i in range(len(candidates[0])):
		target = target_by_most_common(get_most_common(candidates, i))
		candidates = [c for c in candidates if c[i] == target]
		if len(candidates) == 1:
			return candidates[0]

def get_oxygen(diag):
	return find_line_based_on_commonality(diag, lambda x: x)

def get_co2(diag):
	return find_line_based_on_commonality(diag, lambda x: 1 - x)

def to_decimal(array):
	return int(''.join(map(str, array)), 2)

def get_result(reading_a, reading_b):
	diag = get_diagnostics()
	a = reading_a(diag)
	b = reading_b(diag)
	return to_decimal(a) * to_decimal(b)

def test_first():
	assert 2648450 == get_result(get_gamma, get_epsilon)

def test_second():
	assert 2845944 == get_result(get_oxygen, get_co2)
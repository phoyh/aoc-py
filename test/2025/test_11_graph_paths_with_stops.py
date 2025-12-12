import functools as ft

from api import file, parse

def solve(start_vertix: str, example_index: int, is_dac_fft_required: bool) -> int:
	@ft.cache
	def pathes_to_out(vertix: str, has_dac: bool, has_fft: bool) -> int:
		if vertix == 'out':
			return has_dac and has_fft
		return sum(
			pathes_to_out(n, has_dac or (vertix == 'dac'), has_fft or (vertix == 'fft'))
			for n in successors_by_vertix[vertix]
		)

	successors_by_vertix = {
		l[0]: l[1:]
		for l in file.lines(f'2025/11_ex{example_index}', parse.words)
	}
	return pathes_to_out(start_vertix, *[not is_dac_fft_required for _ in range(2)])
	
def test_first():
	assert 5 == solve('you', 1, False)

def test_second():
	assert 2 == solve('svr', 2, True)

import itertools as it

import api.file
import api.parse

def get_series_list():
	return api.file.lines('2023/09', api.parse.ints)

def predict_next(series: list[int]):
	if not any(series):
		return 0
	return series[-1] + predict_next([r - l for l, r in it.pairwise(series)])

def test_first():
	assert 2043183816 == sum(predict_next(s) for s in get_series_list())

def test_second():
	assert 1118 == sum(predict_next(s[::-1]) for s in get_series_list())
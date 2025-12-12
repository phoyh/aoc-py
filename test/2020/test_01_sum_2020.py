import itertools as it
import numpy as np
import api.file

def getProductOfSummands(numberOfSummands):
	ns = [int(l) for l in api.file.lines('2020/01')]
	for indexes in it.product(range(len(ns)), repeat = numberOfSummands):
		if len(set(indexes)) == len(indexes):
			vals = [ns[i] for i in indexes]
			if sum(vals) == 2020:
				return np.prod(vals)

def test_first():
	assert 898299 == getProductOfSummands(2)

def test_second():
	assert 143933922 == getProductOfSummands(3)

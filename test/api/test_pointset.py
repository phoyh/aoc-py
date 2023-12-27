from api import P, PDict, PSet

ex_str = '''
.#####
.#.#.#
##..##
.####.
'''
ex = PSet(PDict.from_lines([str(l) for l in ex_str.split()]).by_value('#'))

def test_transpose():
	assert {(5, 1, 2), (-2, -5, 3)} == PSet({P((2, 1, 5)), P((3, -5, -2))}).transpose()

def test_flood():
	act_wo_diag = ex.flood((3, 2))
	assert (2, 1) in act_wo_diag
	assert (4, 1) not in act_wo_diag
	assert 5 + (5 - 1) + 6 + 4 == len(act_wo_diag)
	act_w_diag = ex.flood((3, 2), diag=True)
	assert (4, 1) in act_w_diag
	assert 5 + 5 + 6 + 4 == len(act_w_diag)

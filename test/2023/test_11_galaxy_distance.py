import itertools as it

from api import PDict, file, P

def solve(open_space_factor):
	galaxies = PDict.from_lines(file.lines('2023/11')).by_value('#')
	expanded_spaces = [
		list(it.accumulate(
			open_space_factor if all(gc != i for gc in gcs) else 1
			for i in range(max(gcs) + 1)
		))
		for gcs in zip(*galaxies)
	]
	expanded_galaxies = {
		P(exp_dim[i] for exp_dim, i in zip(expanded_spaces, g))
		for g in galaxies
	}
	return sum(a.distance(b) for a, b in it.combinations(expanded_galaxies, 2))

def test_first():
	assert 10228230 == solve(2)

def test_second():
	assert 447073334102 == solve(1_000_000)

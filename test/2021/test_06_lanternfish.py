def get_fishes():
	with open('input/2021/06.txt', 'r') as f:
		return list(map(int, f.readlines()[0].strip().split(',')))

def get_population_after(tick_num):
	fishes = get_fishes()
	dist = [fishes.count(i) for i in range(9)]
	for _ in range(tick_num):
		dist = dist[1:] + dist[:1]
		dist[6] += dist[-1]
	return sum(dist)

def test_first():
	assert 360268 == get_population_after(80)

def test_second():
	assert 1632146183902 == get_population_after(256)
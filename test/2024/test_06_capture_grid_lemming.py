import multiprocessing as mp
import itertools as it

from api import file, P, PDict
N, S, W, E = NSWE = P.NSWE()

def get_grid(suffix = ''):
	return PDict.from_lines(file.lines(f'2024/06{suffix}'))

def get_start(g):
	return min(g.by_values('^<v>'))

def is_trapped_with_path(g, obstruction_pos = None):
	pos = get_start(g)
	d = P.by_dir(g[pos])
	walls = g.by_values('#') | {obstruction_pos}
	visited = set()
	vis_w_dir = set()
	while pos in g:
		if (pos, d) in vis_w_dir:
			return True, visited
		visited.add(pos)
		vis_w_dir.add((pos, d))
		nx = pos + d
		if nx in walls:
			d = d.rotate_right()
		else:
			pos = nx
	return False, visited

def test_first():
	_, path = is_trapped_with_path(get_grid())
	assert 5409 == len(path)

def test_second():
	g = get_grid('_ex')
	_, candidates = is_trapped_with_path(g)
	assert 6 == sum(
		is_trapped
		for o in candidates - {get_start(g)}
		for is_trapped, _ in [is_trapped_with_path(g, o)]
	)

#########################

def get_next_wall_idx(wall_idxs, cur_idx, is_dir_incr):
	if len(wall_idxs) == 0:
		return -1
	if cur_idx < wall_idxs[0]:
		return wall_idxs[0] if is_dir_incr else -1
	if cur_idx > wall_idxs[-1]:
		return -1 if is_dir_incr else wall_idxs[-1]
	lower = 0
	upper = len(wall_idxs) - 1
	while lower <= upper:
		mid = (lower + upper) // 2
		if mid + 1 < len(wall_idxs) and wall_idxs[mid] < cur_idx < wall_idxs[mid + 1]:
			return wall_idxs[mid + is_dir_incr]
		if wall_idxs[mid] < cur_idx:
			lower = mid + 1
		else:
			upper = mid - 1
	return -1

def is_trapped_fast(g, obstruction_pos = None):
	"""
	directly jumps to new wall in O(log w) where w is the number of walls in the direction
	only marginally faster than is_trapped_with_path because of cheap steps there
	"""
	pos = min(g.by_values('^<v>'))
	d = P.by_dir(g[pos])
	walls = g.by_values('#')
	if obstruction_pos != pos:
		walls |= {obstruction_pos}
	width, height = g.size_by_dim()
	wall_x_by_y = [
		[x for x in range(width) if (x, y) in walls]
		for y in range(height)
	]
	wall_y_by_x = [
		[y for y in range(height) if (x, y) in walls]
		for x in range(width)
	]
	visited = set()
	vis_w_dir = set()
	while pos in g:
		if (pos, d) in vis_w_dir:
			return True
		visited.add(pos)
		vis_w_dir.add((pos, d))
		px, py = pos
		if d in [N, S]:
			py = get_next_wall_idx(wall_y_by_x[px], py, d == S)
			if py != -1:
				py += 1 if d == N else -1
		if d in [W, E]:
			px = get_next_wall_idx(wall_x_by_y[py], px, d == E)
			if px != -1:
				px += 1 if d == W else -1
		pos = P((px, py))
		while pos + d in walls:
			d = d.rotate_right()
	return False

def test_second_fast():
	g = get_grid('_ex')
	_, candidates = is_trapped_with_path(g)
	assert 6 == sum(
		is_trapped_fast(g, o)
		for o in candidates
	)

################

def get_next_pos_by_pos_dir(g, obstacles, obstacle):
	result = {}
	for d in NSWE:
		start = obstacle - d
		pos = start
		while pos in g and pos not in obstacles:
			result[(pos, d)] = start
			pos -= d
	return result

def get_trapping_obstacle_count(g, candidates):
	"""
	uses a dictionary to find the next wall in O(1) time
	"""
	start_pos = get_start(g)
	start_dir = P.by_dir(g[start_pos])
	walls = g.by_values('#')
	next_pos_by_pos_dir = {
		pos_dir: next_pos
		for w in walls
		for pos_dir, next_pos in get_next_pos_by_pos_dir(g, walls, w).items()
	}
	result = 0
	for o in candidates:
		c_next_by_posdir = next_pos_by_pos_dir | get_next_pos_by_pos_dir(g, walls | {o}, o)
		pos, d = start_pos, start_dir
		vis_w_dir = set()
		while (pos, d) not in vis_w_dir and (pos, d) in c_next_by_posdir:
			vis_w_dir.add((pos, d))
			pos = c_next_by_posdir[(pos, d)]
			d = d.rotate_right()
		if (pos, d) in vis_w_dir:
			result += 1
	return result

def test_second_fastest():
	g = get_grid('_ex')
	_, candidates = is_trapped_with_path(g)
	assert 6 == get_trapping_obstacle_count(g, candidates - {get_start(g)})

################

def is_trapping_obstacle(param):
	g, os, next_pos_by_pos_dir, walls, start_pos, start_dir = param
	result = 0
	for o in os:
		c_next_by_posdir = next_pos_by_pos_dir | get_next_pos_by_pos_dir(g, walls | {o}, o)
		pos, d = start_pos, start_dir
		vis_w_dir = set()
		while (pos, d) not in vis_w_dir and (pos, d) in c_next_by_posdir:
			vis_w_dir.add((pos, d))
			pos = c_next_by_posdir[(pos, d)]
			d = d.rotate_right()
		result += (pos, d) in vis_w_dir
	return result

def get_trapping_obstacle_count_parallel(g, candidates):
	"""
	uses a dictionary to find the next wall in O(1) time
	"""
	start_pos = get_start(g)
	start_dir = P.by_dir(g[start_pos])
	walls = g.by_values('#')
	next_pos_by_pos_dir = {
		pos_dir: next_pos
		for w in walls
		for pos_dir, next_pos in get_next_pos_by_pos_dir(g, walls, w).items()
	}
	batch_size = 1000
	candidate_list = list(candidates)
	sliced_candidates = [
		it.islice(candidate_list, i, i + batch_size)
		for i in range(0, len(candidate_list), batch_size)
	]
	with mp.Pool() as pool:
		trapping_results = pool.map(
			is_trapping_obstacle,
			((g, os, next_pos_by_pos_dir, walls, start_pos, start_dir) for os in sliced_candidates)
		)
		pool.close()
		pool.join()
		return sum(trapping_results)

#def test_second_fastest_parallel():
def do_not_execute_test_second_fastest_parallel():
	"""
	parallel version only 20% faster than fastest single-core version
	-> not part of test suite
	"""
	g = get_grid('')
	_, candidates = is_trapped_with_path(g)
	assert 2022 == get_trapping_obstacle_count_parallel(g, candidates - {get_start(g)})

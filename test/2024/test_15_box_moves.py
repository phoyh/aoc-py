from api import P, PDict, PSet, file, Cube, CubeSet
N, S, W, E = NSWE = P.NSWE()

def get_input(is_expanded=False):
	grid_lines, move_lines = file.segments('2024/15_ex')
	if is_expanded:
		replacements = str.maketrans({'#': '##', 'O': '[]', '.': '..', '@': '@.'})
		grid_lines = [l.translate(replacements) for l in grid_lines]
	g = PDict.from_lines(grid_lines)
	robot = max(g.by_value('@'))
	boxes = g.by_value('[' if is_expanded else 'O')
	walls = g.by_value('#')
	moves = [P.by_dir(s) for s in ''.join(move_lines)]
	return moves, robot, walls, boxes

def move_robot(move_dir, robot, walls, boxes, is_expanded=False):
	moving_coords = PSet({robot})
	moving_boxes = PSet()
	boxes_all_sections = boxes
	if is_expanded:
		boxes_right_section = boxes.move(E)
		boxes_all_sections = boxes | boxes_right_section
	while True:
		new_moving_coords = moving_coords.move(move_dir) - moving_coords
		if new_moving_coords & walls:
			return robot, boxes
		if not new_moving_coords & boxes_all_sections:
			return robot + move_dir, (boxes - moving_boxes) | moving_boxes.move(move_dir)
		new_boxes = new_moving_coords & boxes
		if is_expanded:
			new_boxes |= (new_moving_coords & boxes_right_section).move(W)
			moving_coords |= new_boxes.move(E)
		moving_coords |= new_boxes
		moving_boxes |= new_boxes

def boxes_after_moves(is_expanded=False):
	moves, robot, walls, boxes = get_input(is_expanded)
	for m in moves:
		robot, boxes = move_robot(m, robot, walls, boxes, is_expanded)
	return boxes

def gps_sum(boxes):
	return sum(100 * y + x for x, y in boxes)

def test_first():
	assert 10092 == gps_sum(boxes_after_moves())

def test_second():
	assert 9021 == gps_sum(boxes_after_moves(is_expanded=True))

######## CUBES ########

def move_robot_cubes(move_dir, robot: Cube, walls: CubeSet, boxes: list[Cube]):
	todo = [robot.move(move_dir)]
	moving_box_idxs = set()
	while todo:
		cube_after_move = todo.pop()
		if len(walls & cube_after_move) > 0:
			return robot, boxes
		colliding_box_idxs = [
			i for i, b in enumerate(boxes)
			# additional idx test required because cube might collide with itself
			if cube_after_move & b and i not in moving_box_idxs
		]
		for cb in colliding_box_idxs:
			moving_box_idxs.add(cb)
			todo.append(boxes[cb].move(move_dir))
	new_boxes = [
		b.move(move_dir) if i in moving_box_idxs else b
		for i, b in enumerate(boxes)
	]
	return robot.move(move_dir), new_boxes

def boxes_after_moves_cubes(is_expanded=False):
	moves, robot, walls, boxes = get_input(is_expanded)
	robot = Cube.from_point(robot)
	walls = CubeSet.from_points(walls)
	boxes = [Cube([(x, x + is_expanded), (y, y)]) for x, y in boxes]
	for m in moves:
		robot, boxes = move_robot_cubes(m, robot, walls, boxes)
	return [P(b.min()) for b in boxes]

def test_first_cubes():
	assert 10092 == gps_sum(boxes_after_moves_cubes())

def test_second_cubes():
	assert 9021 == gps_sum(boxes_after_moves_cubes(is_expanded=True))

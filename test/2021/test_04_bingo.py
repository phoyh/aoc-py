import numpy as np
import api.file
import api.parse

def get_boards(sg):
	return [np.array(board_arr) for board_arr in [[api.parse.ints(l) for l in s] for s in sg]]

def get_init_marks(boards):
	return [np.ones_like(b) for b in boards]

def mark(boards, marks, number):
	for b, m in zip(boards, marks):
		m *= b != number

def has_won(mark):
	is_marked = mark == 0
	return (is_marked.all(0) | is_marked.all(1)).any(0)

def board_score(board, mark):
	masked_numbers = board * mark
	return np.sum(np.concatenate(masked_numbers))

def execute_and_get_score(look_for_last = False):
	sg = api.file.segments('2021/04')
	number_draw = api.parse.ints(sg[0][0])
	boards = get_boards(sg[1:])
	marks = get_init_marks(boards)
	for number in number_draw:
		mark(boards, marks, number)
		for i, m in reversed(list(enumerate(marks))):
			if has_won(m):
				if not look_for_last or len(boards) == 1:
					return number * board_score(boards[i], m)
				boards.pop(i)
				marks.pop(i)

def test_first():
	assert 14093 == execute_and_get_score()

def test_second():
	assert 17388 == execute_and_get_score(True)
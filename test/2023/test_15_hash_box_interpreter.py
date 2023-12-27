import functools as ft
import re

from api import file

def get_commands():
	return file.readall('2023/15').split(',')

def get_hash(s):
	return ft.reduce(lambda v, c: ((v + ord(c)) * 17) % 256, s, 0)

def get_boxes_after_commands(commands):
	boxes = [{} for _ in range(256)]
	for c in commands:
		label, focal_length = re.split(r'[-=]', c)
		box = boxes[get_hash(label)]
		if focal_length:
			box[label] = int(focal_length)
		else:
			box.pop(label, None)
	return boxes

def test_first():
	assert 511498 == sum(map(get_hash, get_commands()))

def test_second():
	boxes = get_boxes_after_commands(get_commands())
	lense_powers = [
		box_nr * slot_nr * focal_length
		for box_nr, box in enumerate(boxes, 1)
		for slot_nr, focal_length in enumerate(box.values(), 1)
	]
	assert 284674 == sum(lense_powers)

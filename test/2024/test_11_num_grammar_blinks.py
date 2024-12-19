import functools as ft
from api import file, parse

def get_stones():
	return file.readall('2024/11', parse.ints)

@ft.cache
def stone_count(stone: int, blinks):
	if blinks == 0:
		return 1
	if stone == 0:
		return stone_count(1, blinks - 1)
	s = str(stone)
	sl = len(s)
	if sl % 2 == 0:
		return sum(
			stone_count(int(part), blinks - 1)
			for part in (s[:sl//2], s[sl//2:])
		)
	return stone_count(stone * 2024, blinks - 1)

def get_total_stone_count_after_blinks(blinks):
	return sum(stone_count(s, blinks) for s in get_stones())

def test_first():
	assert 203457 == get_total_stone_count_after_blinks(25)

def test_second():
	assert 241394363462435 == get_total_stone_count_after_blinks(75)

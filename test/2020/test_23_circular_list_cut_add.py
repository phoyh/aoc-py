import functools as ft
from api import file

def get_cups():
	return [int(e) for e in file.readall('2020/23')]

def solve(cups, moves: int, fill_up_to: int):
	min_cup, max_cup = min(cups), max(cups)
	if fill_up_to > max_cup:
		cups += list(range(max_cup + 1, fill_up_to + 1))
		max_cup = fill_up_to
	next_cup = {cups[i]: cups[(i + 1) % len(cups)] for i in range(len(cups))}
	current = cups[0]
	for _ in range(moves):
		pickups = [next_cup[current], next_cup[next_cup[current]], next_cup[next_cup[next_cup[current]]]]
		next_cup[current] = next_cup[pickups[-1]]
		dest_value = current
		while dest_value in pickups + [current]:
			dest_value -= 1
			if dest_value < min_cup:
				dest_value = max_cup
		next_cup[pickups[-1]] = next_cup[dest_value]
		next_cup[dest_value] = pickups[0]
		current = next_cup[current]
	result = []
	current = 1
	for _ in range(len(cups) - 1):
		current = next_cup[current]
		result.append(current)
	return result

def test_first():
	result = solve(get_cups(), 100, 0)
	assert 95648732 == ft.reduce(lambda x, y: x * 10 + y, result, 0)

#def test_second():
#	result = solve(get_cups(), int(1e7), int(1e6))
#	assert 192515314252 == result[0] * result[1]

def test_second_abbreviated():
	result = solve(get_cups(), int(1e3), int(1e2))
	assert 68 * 13 == result[0] * result[1]

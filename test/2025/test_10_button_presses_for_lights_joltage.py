import itertools as it
import z3

from api import file, parse, z3result

def parse_line(line: str):
	lightstr, *buttonstrs, joltagestr = line.split()
	lights = [c == '#' for c in lightstr[1:-1]]
	buttons = [parse.ints(bs) for bs in buttonstrs]
	joltage = parse.ints(joltagestr)
	return lights, buttons, joltage

def get_lines():
	return file.lines('2025/10_ex', parse_line)

def get_min_button_press_lights(target_lights, buttons):
	result = len(buttons)
	for is_pressed_by_button_idx in it.product(range(2), repeat=len(buttons)):
		lights = [False for _ in target_lights]
		for button, is_pressed in zip(buttons, is_pressed_by_button_idx):
			if is_pressed:
				for li in button:
					lights[li] = not lights[li]
		if lights == target_lights:
			result = min(result, sum(is_pressed_by_button_idx))
	return result

def get_min_button_press_joltage(target_joltage, buttons):
	z3bs = [z3.Int(f'b_{bi}') for bi in range(len(buttons))]
	z3press_count = z3.Int('press_count')
	o = z3.Optimize()
	for z3b in z3bs:
		o.add(z3b >= 0)
	for ji, tj in enumerate(target_joltage):
		o.add(tj == z3.Sum([
			z3b
			for z3b, b in zip(z3bs, buttons)
			if ji in b
		]))
	o.add(z3press_count == z3.Sum(z3bs))
	min_cost = z3result.minimize(o, z3press_count)
	assert min_cost is not None
	return min_cost

def test_first():
	assert 7 == sum(
		get_min_button_press_lights(target_lights, buttons)
		for target_lights, buttons, _ in get_lines()
	)

def test_second():
	assert 33 == sum(
		get_min_button_press_joltage(target_joltage, buttons)
		for _, buttons, target_joltage in get_lines()
	)
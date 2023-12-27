from collections import defaultdict, deque
import math

from api import file

def get_modules():
	downstream = {}
	flipflops = {}
	conjunctions = {}
	for l in file.lines('2023/20'):
		mod, lr = l.split(' -> ')
		match mod[0]:
			case '%':
				mod = mod[1:]
				flipflops[mod] = False
			case '&':
				mod = mod[1:]
				conjunctions[mod] = None
		downstream[mod] = lr.split(', ')
	conjunctions = {
		c: {fromwhere: False for fromwhere, towheres in downstream.items() if c in towheres}
		for c in conjunctions
	}
	return downstream, flipflops, conjunctions

def press_button(downstream, flipflops, conjunctions):
	todo = deque([(str('button'), str('broadcaster'), bool(False))])
	signal_stat = defaultdict(int)
	while todo:
		fromwhere, mod, signal = todo.popleft()
		signal_stat[(fromwhere, signal)] += 1
		downstream_signal = None
		if mod in flipflops:
			if not signal:
				downstream_signal = flipflops[mod] = not flipflops[mod]
		elif mod in conjunctions:
			conjunctions[mod][fromwhere] = signal
			downstream_signal = not all(conjunctions[mod].values())
		else:
			downstream_signal = signal
		if downstream_signal is not None and mod in downstream:
			for d in downstream[mod]:
				todo.append((mod, d, downstream_signal))
	return signal_stat

def test_first():
	downstream, flipflops, conjunctions = get_modules()
	low = 0
	high = 0
	for _ in range(1000):
		signal_stat = press_button(downstream, flipflops, conjunctions)
		for (_, signal), occ in signal_stat.items():
			if signal:
				high += occ
			else:
				low += occ
	assert 680278040 == low * high

def test_second():
	downstream, flipflops, conjunctions = get_modules()
	last_conj = next(mod for mod, downs in downstream.items() if 'rx' in downs)
	last_conj_froms = {
		lcf: 0
		for lcf in conjunctions[last_conj]
	}
	button_presses = 0
	while not all(last_conj_froms.values()):
		button_presses += 1
		signal_stat = press_button(downstream, flipflops, conjunctions)
		for lcf in last_conj_froms:
			if not last_conj_froms[lcf] and (lcf, True) in signal_stat:
				last_conj_froms[lcf] = button_presses
	assert 243548140870057 == math.lcm(*last_conj_froms.values())

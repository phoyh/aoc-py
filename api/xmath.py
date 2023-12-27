"""
Provides math utilities that go beyond math.
"""

from typing import TypeVar, Callable

TK = TypeVar('TK')
TNum = TypeVar('TNum', int, float)

def argmax_max(keys: set[TK] | list[TK], value_function: Callable[[TK], TNum], default: TNum = 0) \
		-> tuple[list[TK], TNum]:
	if len(keys) == 0:
		return [], default
	if not isinstance(keys, list):
		keys = list(keys)
	values = [value_function(k) for k in keys]
	ma = max(values)
	return [k for k, v in zip(keys, values) if v == ma], ma

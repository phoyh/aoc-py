"""
Provides math utilities that go beyond math.
"""

import math

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

def argmin_min(keys: set[TK] | list[TK], value_function: Callable[[TK], TNum], default: TNum = 0) \
		-> tuple[list[TK], TNum]:
	mins, max_value = argmax_max(keys, lambda k: -value_function(k), -default)
	return mins, -max_value

def chinese_remainder(remainders: list[int], moduli: list[int]) -> int:
	prod_moduli = math.prod(moduli)
	result = sum(
		prod_other_moduli * remainder * __chinese_remainder_second_inverse(modulo, prod_other_moduli)
		for remainder, modulo in zip(remainders, moduli)
		for prod_other_moduli in [prod_moduli // modulo]
	)
	return result % prod_moduli

def __chinese_remainder_second_inverse(first, second):
	"""
	multiplicative inverse
	x0 * first + RESULT * second = gcd(x0, RESULT)
	"""
	x, y = first, second
	x0, x1, y0, y1 = 1, 0, 0, 1
	while y > 0:
		gcd, x, y = x // y, y, x % y
		x0, x1 = x1, x0 - gcd * x1
		y0, y1 = y1, y0 - gcd * y1
	return y0

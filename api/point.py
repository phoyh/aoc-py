from __future__ import annotations
import itertools as it
from typing import Any

# for NSWE usage:
# N, S, W, E = NSWE = Point.NSWE()

# needed for relaxing parameters to non Point tuples
# never to be used for returning types (must be as specific as possible)
TP = tuple[int,...]

class P(TP):
	"""
	Grid utilities for one coordinate (point).

	All operations are FUNCTIONAL (without side-effects) and
	always return a new instance for the result.
	"""

	@classmethod
	def NSWE(cls):
		return [P(p) for p in [(0, -1), (0, 1), (-1, 0), (1, 0)]]

	@classmethod
	def O(cls):
		return P((0, 0))

	@classmethod
	def box(cls, p: P | TP) -> P:
		return p if isinstance(p, P) else P(p)
	
	@classmethod
	def by_dir(cls, d: str) -> P:
		"""
		Understands cardinal orientations (NSWE), directions (UDLR) and symbols (^v<>).

		Note that UL and ^< is NW.

		Can also cope with full denominations (south, West, left).
		"""
		alternatives = ['UDLR', '^v<>']
		c = d[0].upper().translate(str.maketrans(
			''.join(alternatives).upper(),
			'NSWE' * len(alternatives)
		))
		return cls.NSWE()['NSWE'.index(c)]

	# basic operators

	def __add__(self, other: TP) -> P:
		return P(ax + bx for ax, bx in zip(self, other))

	def __sub__(self, other: TP) -> P:
		return P(ax - bx for ax, bx in zip(self, other))

	def __mul__(self, f: int) -> P:
		return P(ac * f for ac in self)

	def __floordiv__(self, f: int) -> P:
		return P(ac // f for ac in self)

	def __neg__(self) -> P:
		return P(-ac for ac in self)

	def __mod__(self, other: TP) -> P:
		return P(ac % oc for ac, oc in zip(self, other))

	# utilities

	def distance(self, point_any_dim2: TP, diag: bool = False) -> int:
		comp_dist = [abs(a - b) for a, b in zip(self, point_any_dim2)]
		return max(comp_dist) if diag else sum(comp_dist)

	def neighbors(self, diag: bool = False,
			within: TPSet | dict[P, Any] | None = None,
			dist: int = 1) -> PSet:
		dims = len(self)
		res = PSet()
		for delta in it.product(range(-dist, dist + 1), repeat=dims):
			candidate = P(e + de for e, de in zip(self, delta))
			cand_dist = sum(abs(x) for x in delta)
			if candidate != self and (diag or cand_dist <= dist):
				if within is None or candidate in within:
					res.add(candidate)
		return res

	def to_cube(self) -> Cube:
		iv = [(pc, pc) for pc in self]
		return Cube(iv)

	def transpose(self) -> P:
		return P(self[::-1])

# late import to allow cyclic references between cube(set) and point(dict/list/set)
# pylint: disable=wrong-import-position
from .cube import Cube
from .pointset import PSet, TPSet
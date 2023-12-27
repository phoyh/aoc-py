from __future__ import annotations
import itertools as it
from typing import TypeVar, Any, Callable
import numpy as np

from .point import P, TP

TV = TypeVar('TV')

# Yes, there are many methods - but this is a very versatile class
# pylint: disable-next=too-many-public-methods
class PDict(dict[P, TV]):
	"""
	Grid utilities for a dictionary which maps points to values (not necessarily ints).

	All operations are FUNCTIONAL (without side-effects) and
	always return a new instance for the result.

	Drawing operations on the dictionary return same dictionary type (dict vs. defaultdict),
	complete transformations do not.
	"""

	# OVERRIDE

	def __or__(self, other: dict[P, TV]) -> PDict:
		return PDict(dict.__or__(self, other))

	def copy(self) -> PDict:
		return PDict(dict.copy(self))

	def keys(self) -> PSet:
		return PSet(dict.keys(self))
	
	# DIMENSIONS (FACADE FOR KEY SETS)

	def max_by_dim(self) -> list[int]:
		return self.keys().max_by_dim()

	def minmax_by_dim(self) -> list[tuple[int, int]]:
		return self.keys().minmax_by_dim()

	def range_by_dim(self) -> list[range]:
		return self.keys().range_by_dim()

	def size_by_dim(self) -> list[int]:
		return self.keys().size_by_dim()

	# EXTENSIONS

	def by_value(self, value_for_which_points_are_found: TV) \
			-> PSet:
		return PSet({p for p, v in self.items() if v == value_for_which_points_are_found})

	def by_not_value(self, value_for_which_points_are_excluded: TV) \
			-> PSet:
		return PSet({p for p, v in self.items() if v != value_for_which_points_are_excluded})

	def by_values(self, values_for_which_points_are_found: set[TV] | list[TV] | str) \
			-> PSet:
		"""
		String can be provided as parameter if TV is char.
		"""
		if isinstance(values_for_which_points_are_found, str):
			vals = set(values_for_which_points_are_found)
		elif isinstance(values_for_which_points_are_found, list):
			vals = set(values_for_which_points_are_found)
		else:
			vals = values_for_which_points_are_found
		return PSet({p for p, v in self.items() if v in vals})

	def diff_points(self, other: dict[P, TV]) -> PSet:
		one_sided = lambda d1, d2: PSet(
			{d1k for d1k, d1v in d1.items() if d1k not in d2 or d2[d1k] != d1v}
		)
		return one_sided(self, other) | one_sided(other, self)

	def draw_line(self, start_point: TP, end_point: TP,
			value_to_be_drawn: TV) -> PDict:
		""" assert that line is horizontal, vertical or diagonal """
		result = self.copy()
		p = np.array(start_point)
		e = np.array(end_point)
		assert len(p) == len(e)
		bearing = np.sign(e - p)
		if (bearing == 0).all():
			result[P(p)] = value_to_be_drawn
			return result
		steps_per_dim = bearing * (e - p)
		steps = max(steps_per_dim)
		assert ((steps_per_dim == 0) | (steps_per_dim == steps)).all()
		while (p != e + bearing).any():
			result[P(p)] = value_to_be_drawn
			p += bearing
		return result

	def draw_set(self, points_where_to_draw: TPSet,
			value_to_be_drawn: TV) -> PDict:
		result = self.copy()
		for p in points_where_to_draw:
			result[p] = value_to_be_drawn
		return result

	def flood(self, flood_value: TV, start_point: TP, diag: bool = False) \
			-> PDict:
		"""
		Fills with 'flood_value' on starting point and any (transitively) adjacent points
		that have same value as starting point

		Note: That means tolerance = 0
		"""
		start_point = P.box(start_point)
		result = self.copy()
		source_value = self[start_point]
		todo = {start_point}
		while todo:
			p = todo.pop()
			if self[p] == source_value and result[p] != flood_value:
				result[p] = flood_value
				todo |= p.neighbors(diag, self)
		return result

	def fringe(self, diag: bool = False) -> PDict:
		return PDict({p: self[p] for p in self.keys().fringe(diag = diag)})

	def move(self, vector: TP) -> PDict:
		return PDict({p + vector: value for p, value in self.items()})

	def pad(self, value: TV, diag: bool = False, distance: int = 1) \
			-> PDict:
		return PDict({
			n: value
			for p in self.fringe()
			for n in p.neighbors(diag=diag, dist=distance)
		} | self)

	def transpose(self) -> PDict:
		return PDict({p.transpose(): v for p, v in self.items()})

	# IMPORT / EXPORT

	@staticmethod
	def from_lines(lines_with_char1_values: list[str],
			value_mapper: Callable[[str], Any] = lambda c: c) -> PDict:
		return PDict({
			P((x, y)): value_mapper(v)
			for y, l in enumerate(lines_with_char1_values)
			for x, v in enumerate(l)
		})

	@staticmethod
	def from_minmax(minmax_by_dim: list[tuple[int, int]], value: TV) -> PDict:
		result = PDict()
		for p in it.product(*[range(mi, ma + 1) for mi, ma in minmax_by_dim]):
			result[P(p)] = value
		return result

	@staticmethod
	def from_size(length_by_dim: list[int], value: TV) -> PDict:
		result = PDict()
		for p in it.product(*[range(lbd) for lbd in length_by_dim]):
			result[P(p)] = value
		return result

	def to_complex_keys_2d(self) -> dict[complex, TV]:
		return {complex(x, y): v for (x, y), v in self.items()}

	def to_lines_2d(self) -> list[str]:
		(minx, maxx), (miny, maxy), *_ = self.keys().minmax_by_dim()
		matrix = np.full((maxy - miny + 1, maxx - minx + 1), ' ')
		for x, y in self:
			matrix[y - miny, x - minx] = self[P((x, y))]
		return [''.join(l) for l in matrix]

	def to_str_2d(self) -> str:
		return '\n'.join(self.to_lines_2d())

# late import to allow cyclic references between cube(set) and point(dict/list/set)
# pylint: disable=wrong-import-position
from .pointset import PSet, TPSet

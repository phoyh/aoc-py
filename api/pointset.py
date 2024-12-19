from __future__ import annotations

import itertools as it
from .point import P, TP

# needed for relaxing parameters to non PointSet sets
# never to be used for returning types (must be as specific as possible)
TPSet = set[P]

class PSet(TPSet):
	"""
	Grid utilities for a set of points.

	All operations are FUNCTIONAL (without side-effects) and
	always return a new instance for the result.
	"""

	# OVERRIDE

	def __and__(self, other: TPSet | list[P]) -> PSet:
		if isinstance(other, list):
			other = set(other)
		return PSet(set.__and__(self, other))

	def __or__(self, other: TPSet | list[P]) -> PSet:
		if isinstance(other, list):
			other = set(other)
		return PSet(set.__or__(self, other))

	def __sub__(self, other: TPSet | list[P]) -> PSet:
		if isinstance(other, list):
			other = set(other)
		return PSet(set.__sub__(self, other))

	def copy(self) -> PSet:
		return PSet(set.copy(self))

	# DIMENSIONS

	def max_by_dim(self) -> list[int]:
		return [max(p) for p in zip(*self)]

	def minmax_by_dim(self) -> list[tuple[int, int]]:
		return [(min(p), max(p)) for p in zip(*self)]

	def range_by_dim(self) -> list[range]:
		return [range(mi, ma + 1) for mi, ma in self.minmax_by_dim()]

	def size_by_dim(self) -> list[int]:
		return [ma - mi + 1 for mi, ma in self.minmax_by_dim()]

	# DERIVE NEW POINTSET

	def edges(self, diag: bool = False) -> set[tuple[P, P]]:
		"""
		Returns a set of all tuples representing an edge between two points:
		one on the inside and one on the outside.
		"""
		return {(p, n) for p in self for n in p.neighbors(diag=diag) if n not in self}

	def flood(self, start_point: TP, diag: bool = False) \
			-> PSet:
		"""
		Floods starting with 'start_point' until encountering elements of Self set.
		
		Self set must have proper boundary entries so that this flooding DOES NOT CONTINUE INFINITELY.

		Returns Self plus the set of points which were flooded (including 'start_point' if it was valid).
		"""
		result = self.copy()
		todo = {P.box(start_point)}
		while todo:
			p = todo.pop()
			if p not in result:
				result.add(p)
				todo |= p.neighbors(diag)
		return result

	def fringe(self, diag: bool = False) -> PSet:
		return PSet({p for p in self if p.neighbors(diag) - self})

	def move(self, vector: TP) -> PSet:
		return PSet({p + vector for p in self})

	def transpose(self) -> PSet:
		return PSet({p.transpose() for p in self})

	# IMPORT / EXPORT

	@staticmethod
	def from_minmax(minmax_by_dim: list[tuple[int, int]]) -> PSet:
		return PSet({
			P(p)
			for p in it.product(*[range(mi, ma + 1) for mi, ma in minmax_by_dim])
		})

	@staticmethod
	def from_size(length_by_dim: list[int]) -> PSet:
		return PSet({
			P(p)
			for p in it.product(*[range(lbd) for lbd in length_by_dim])
		})

	def to_lines_2d(self) -> list[str]:
		g = PDict().draw_set(self, '#')
		return g.to_lines_2d()

	def to_png(self, file_name: str, file_dir: str = ''):
		"""
		Exports the dictionary as a PNG file.
		The [file_path/file_name] is relative to ./exports and should not contain the extension.
		"""
		g = PDict().draw_set(self, (255, 255, 255))
		g.to_png(file_name, file_dir)

	def to_str_2d(self) -> str:
		return '\n'.join(self.to_lines_2d())

# late import to allow cyclic references between cube(set) and point(dict/list/set)
# pylint: disable=wrong-import-position
from .pointdict import PDict

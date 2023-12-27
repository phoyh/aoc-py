from __future__ import annotations

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

	def __and__(self, other: TPSet) -> PSet:
		return PSet(set.__and__(self, other))

	def __or__(self, other: TPSet) -> PSet:
		return PSet(set.__or__(self, other))

	def __sub__(self, other: TPSet) -> PSet:
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

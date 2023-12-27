from __future__ import annotations
import itertools as it

from .point import P, TP

# needed for relaxing parameters to non PointList lists
# never to be used for returning types (must be as specific as possible)
TPList = list[P]

class PList(TPList):
	"""
	Grid utilities for list of points.

	All operations are FUNCTIONAL (without side-effects) and
	always return a new instance for the result.
	"""

	# OVERRIDE

	def copy(self) -> PList:
		return PList(list.copy(self))
	
	# EXTENSIONS

	def move(self, vector: TP) -> PList:
		return PList([p + vector for p in self])

	def surface_2d(self) -> int:
		"""
		Interpretes adjacent point-pairs as lines and calculates the surface enclosed by them.

		Only provides meaningful result if lines are not overlapping.

		Auto-completes path if last point is not the first one.
		"""
		if self[0] == self[-1]:
			corners = self
		else:
			corners = self + [self[0]]
		lines2 = area2 = 0
		# shoelace trapzoid formula
		# - add half of the lines:
		#   - line drawn in the middle of the "cells" covering half of it on average
		#   - line length according to Chebyshev because question is how many '#' get painted
		# - add area separately and abs at the end (clock/count-clock lead only to different sign)
		for a, b in it.pairwise(corners):
			ax, ay = a
			bx, by = b
			area2 += (bx - ax) * (ay + by)
			lines2 += a.distance(b, diag=True)
		return 1 + (lines2 + abs(area2)) // 2

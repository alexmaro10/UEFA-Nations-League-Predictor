from __future__ import annotations

import math
import random


def sample_poisson(lmbda: float) -> int:
	"""
	Generate one Poisson-distributed random value.

	Uses Knuth's algorithm.
	"""

	if lmbda <= 0:
		return 0

	limit = math.exp(-lmbda)

	probability = 1.0

	goals = 0

	while probability > limit:

		goals += 1

		probability *= random.random()

	return goals - 1
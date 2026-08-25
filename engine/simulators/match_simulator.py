from __future__ import annotations

from copy import deepcopy

from engine.models.expected_goals import (
	calculate_expected_goals,
)
from engine.probability.poisson import sample_poisson

from models.match import Match


def simulate_match(match: Match) -> Match:
	"""
	Simulate a single football match.

	Returns
	-------
	Match
		A copy of the original match containing the simulated score.
	"""

	simulated_match = match.copy()

	home_lambda, away_lambda = calculate_expected_goals(
		simulated_match.home,
		simulated_match.away,
		match.local
	)

	simulated_match.home_goals = sample_poisson(home_lambda)

	simulated_match.away_goals = sample_poisson(away_lambda)

	simulated_match.played = True

	return simulated_match
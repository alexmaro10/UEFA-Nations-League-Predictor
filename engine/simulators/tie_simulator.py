from __future__ import annotations

import random

from copy import deepcopy

from engine.models.expected_goals import (
	calculate_expected_goals,
)
from engine.simulators.match_simulator import simulate_match
from engine.probability.poisson import sample_poisson

from models.match import Match
from models.tie import Tie
from models.team import Team

def simulate_tie(tie: Tie) -> Tie:
	simulated_tie = tie.copy()

	simulated_tie.first_match = simulate_match(simulated_tie.first_match)
	simulated_tie.second_match = simulate_match(simulated_tie.second_match)

	team1_goals = simulated_tie.first_match.home_goals + simulated_tie.second_match.away_goals
	team2_goals = simulated_tie.first_match.away_goals + simulated_tie.second_match.home_goals
	
	if team1_goals > team2_goals:
		simulated_tie.winner = simulated_tie.first_match.home
		simulated_tie.first_match.winner = simulated_tie.first_match.home
		simulated_tie.second_match.winner = simulated_tie.first_match.home
	elif team1_goals < team2_goals:
		simulated_tie.winner = simulated_tie.first_match.away
		simulated_tie.first_match.winner = simulated_tie.first_match.away
		simulated_tie.second_match.winner = simulated_tie.first_match.away
	else:
		teams = [
			simulated_tie.first_match.home,
			simulated_tie.first_match.away
		]
		simulated_tie.winner = random.choice(teams)
		simulated_tie.state = "Penaltis"

	return simulated_tie
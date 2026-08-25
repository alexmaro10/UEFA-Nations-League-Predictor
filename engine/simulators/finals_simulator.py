from __future__ import annotations

import random

from copy import deepcopy

from engine.models.expected_goals import (
	calculate_expected_goals,
)
from engine.simulators.match_simulator import simulate_match
from engine.probability.poisson import sample_poisson

from models.match import Match
from models.final_four import Final_Four
from models.team import Team

def simulate_finals(final_four: Final_Four) -> Final_Four:
	simulated_final = final_four.final.copy()

	team1 = simulated_final.home
	team2 = simulated_final.away

	simulated_final = simulate_match(simulated_final)

	team1_goals = simulated_final.home_goals
	team2_goals = simulated_final.away_goals

	final_four.final = simulated_final

	if team1_goals > team2_goals:
		final_four.winner_final = team1
		final_four.losser_final = team2
	elif team1_goals < team2_goals:
		final_four.winner_final = team2
		final_four.losser_final = team1
	else:
		teams = [team1,team2]
		final_four.winner_final = random.choice(teams)
		teams.remove(final_four.winner_final)
		final_four.losser_final = random.choice(teams)
	
	simulated_third_place = final_four.third_place.copy()

	team1 = simulated_third_place.home
	team2 = simulated_third_place.away

	simulated_third_place = simulate_match(simulated_third_place)

	team1_goals = simulated_third_place.home_goals
	team2_goals = simulated_third_place.away_goals

	final_four.third_place = simulated_third_place

	if team1_goals > team2_goals:
		final_four.winner_third = team1
		final_four.losser_third = team2
	elif team1_goals < team2_goals:
		final_four.winner_third = team2
		final_four.losser_third = team1
	else:
		teams = [team1,team2]
		final_four.winner_third = random.choice(teams)
		teams.remove(final_four.winner_third)
		final_four.losser_third = random.choice(teams)

	final_four.final.winner = final_four.winner_final
	final_four.third_place.winner = final_four.winner_third

	return final_four

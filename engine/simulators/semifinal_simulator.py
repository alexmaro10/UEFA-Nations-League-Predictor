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

def simulate_semifinals(final_four: Final_Four) -> Final_Four:
	simulated_sf1 = final_four.semi_final1.copy()

	team1 = simulated_sf1.home
	team2 = simulated_sf1.away

	simulated_sf1 = simulate_match(simulated_sf1)

	team1_goals = simulated_sf1.home_goals
	team2_goals = simulated_sf1.away_goals

	final_four.semi_final1 = simulated_sf1

	if team1_goals > team2_goals:
		final_four.winner_sf1 = team1
		final_four.losser_sf1 = team2
	elif team1_goals < team2_goals:
		final_four.winner_sf1 = team2
		final_four.losser_sf1 = team1
	else:
		teams = [team1,team2]
		final_four.winner_sf1 = random.choice(teams)
		teams.remove(final_four.winner_sf1)
		final_four.losser_sf1 = random.choice(teams)
	
	simulated_sf2 = final_four.semi_final2.copy()

	team1 = simulated_sf2.home
	team2 = simulated_sf2.away

	simulated_sf2 = simulate_match(simulated_sf2)

	team1_goals = simulated_sf2.home_goals
	team2_goals = simulated_sf2.away_goals

	final_four.semi_final2 = simulated_sf2

	if team1_goals > team2_goals:
		final_four.winner_sf2 = team1
		final_four.losser_sf2 = team2
	elif team1_goals < team2_goals:
		final_four.winner_sf2 = team2
		final_four.losser_sf2 = team1
	else:
		teams = [team1,team2]
		final_four.winner_sf2 = random.choice(teams)
		teams.remove(final_four.winner_sf2)
		final_four.losser_sf2 = random.choice(teams)

	final_four.semi_final1.winner = final_four.winner_sf1
	final_four.semi_final2.winner = final_four.winner_sf2
	final_four.third_place = Match(
		id= 2001,
		phase="thrid_place",
		group = "",
		matchday = 10,
		home = final_four.losser_sf1,
		away = final_four.losser_sf2,
		played = False,
		home_goals = 0,
		away_goals = 0,
		winner = None,
		losser = None,
		local = False
	)
	final_four.final = Match(
		id= 2000,
		phase="final",
		group = "",
		matchday = 10,
		home = final_four.winner_sf1,
		away = final_four.winner_sf2,
		played = False,
		home_goals = 0,
		away_goals = 0,
		winner = None,
		losser = None,
		local = False
	)

	return final_four

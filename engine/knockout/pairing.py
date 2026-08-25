from __future__ import annotations

import random

from engine.knockout.restrictions import get_valid_opponents

from models.ranking import Ranking
from models.match import Match
from models.tie import Tie
from models.team import Team


def pair_rankings(
	seeded: Ranking,
	unseeded: Ranking,
	teams: dict[str, Team],
	iden: int,
	same_group_forbidden: bool = True,
) -> list[Tie] | None:
	"""
	Pair two rankings into knockout ties.
	"""

	available_opponents = unseeded.standings.copy()

	seeded_teams = seeded.standings.copy()
	random.shuffle(seeded_teams)

	ties: list[Tie] = []

	for standing in seeded_teams:

		valid_opponents = get_valid_opponents(
			standing,
			available_opponents,
			same_group_forbidden,
		)

		if not valid_opponents:
			return None

		opponent = random.choice(valid_opponents)

		available_opponents.remove(opponent)

		if iden == 0:
			ties.append(
				Tie(
					name="",
					first_match= Match(
						id= 156+len(ties),
						phase="quarter-finals",
						group = "",
						matchday = 7,
						home = teams[opponent.team.code],
						away = teams[standing.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					),
					second_match = Match(
						id= 156+len(ties)+8,
						phase="quarter-finals",
						group = "",
						matchday = 8,
						home = teams[standing.team.code],
						away = teams[opponent.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					)
				)
			)
		if iden == 1:
			ties.append(
				Tie(
					name="",
					first_match= Match(
						id= 172+len(ties),
						phase="playoffs ab",
						group = "",
						matchday = 9,
						home = teams[opponent.team.code],
						away = teams[standing.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					),
					second_match = Match(
						id= 172+len(ties)+4,
						phase="playoffs ab",
						group = "",
						matchday = 10,
						home = teams[standing.team.code],
						away = teams[opponent.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					)
				)
			)
		if iden == 2:
			ties.append(
				Tie(
					name="",
					first_match= Match(
						id= 180+len(ties),
						phase="playoffs bc",
						group = "",
						matchday = 11,
						home = teams[opponent.team.code],
						away = teams[standing.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					),
					second_match = Match(
						id= 180+len(ties)+4,
						phase="playoffs bc",
						group = "",
						matchday = 12,
						home = teams[standing.team.code],
						away = teams[opponent.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					)
				)
			)
		if iden == 3:
			ties.append(
				Tie(
					name="",
					first_match= Match(
						id= 188+len(ties),
						phase="playoffs cd",
						group = "",
						matchday = 13,
						home = teams[opponent.team.code],
						away = teams[standing.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					),
					second_match = Match(
						id= 188+len(ties)+4,
						phase="playoffs cd",
						group = "",
						matchday = 14,
						home = teams[standing.team.code],
						away = teams[opponent.team.code],
						played = False,
						home_goals = 0,
						away_goals = 0,
						winner = None,
						losser = None,
						local = True
					)
				)
			)

	return ties
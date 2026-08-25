from __future__ import annotations

from collections import defaultdict

from models.ranking import Ranking
from models.standing import Standing

def build_rankings(standings: dict[str, list[Standing]]) -> dict[str, Ranking]:
	
	ranking_standings: dict[str, list[Standing]] =defaultdict(list)

	for group_name, table in standings.items():
		league = group_name[0]
		for position, standing in enumerate(table, start=1):
			ranking_name= f"{league}{position}"
			ranking_standings[ranking_name].append(standing)
	
	rankings: dict[str, Ranking] = {}

	for ranking_name, table in ranking_standings.items():
		table.sort(
			key=lambda s:(
				-s.points,
				-s.goal_difference,
				-s.goals_for,
			)
		)

		rankings[ranking_name] = Ranking(
			name=ranking_name,
			standings=table
		)

	return rankings

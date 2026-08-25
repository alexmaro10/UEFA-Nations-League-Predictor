from __future__ import annotations

from models.ranking import Ranking
from models.tie import Tie

from engine.knockout.pairing import pair_rankings


def build_playoffs_bc(
	league_b_third: Ranking,
	league_c_second: Ranking,
	teams: dict[str, Team]
) -> list[Tie]:
	"""
	Build the League B/C promotion/relegation play-offs.
	"""

	playoffs = pair_rankings(
		unseeded=league_c_second,
		seeded=league_b_third,
		same_group_forbidden=True,
		teams = teams,
		iden = 2
	)

	for i, tie in enumerate(playoffs, start=1):
		tie.name = f"BC{i}"

	return playoffs
from __future__ import annotations

from models.ranking import Ranking
from models.tie import Tie

from engine.knockout.pairing import pair_rankings


def build_playoffs_ab(
	league_a_third: Ranking,
	league_b_second: Ranking,
	teams: dict[str, Team]
) -> list[Tie]:
	"""
	Build the League A/B promotion/relegation play-offs.
	"""

	playoffs = pair_rankings(
		unseeded=league_b_second,
		seeded=league_a_third,
		same_group_forbidden=True,
		teams = teams,
		iden = 1
	)

	for i, tie in enumerate(playoffs, start=1):
		tie.name = f"AB{i}"

	return playoffs
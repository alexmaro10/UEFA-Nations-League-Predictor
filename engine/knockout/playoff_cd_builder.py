from __future__ import annotations

from models.ranking import Ranking
from models.tie import Tie

from engine.knockout.pairing import pair_rankings


def build_playoffs_cd(
	league_c_fourth: Ranking,
	league_d_second: Ranking,
	teams: dict[str, Team]
) -> list[Tie]:
	"""
	Build the League C/D promotion/relegation play-offs.

	Only the two best fourth-placed teams from League C
	take part in the play-offs.
	"""

	best_fourths = Ranking(
		name="C4_PLAYOFF",
		standings=league_c_fourth.standings[:2],
	)

	playoffs = pair_rankings(
		unseeded=league_d_second,
		seeded=best_fourths,
		same_group_forbidden=True,
		teams = teams,
		iden = 3
	)

	for i, tie in enumerate(playoffs, start=1):
		tie.name = f"CD{i}"

	return playoffs
from __future__ import annotations

from models.ranking import Ranking
from models.tie import Tie

from engine.knockout.pairing import pair_rankings


def build_quarter_finals(
	winners: Ranking,
	runners_up: Ranking,
	teams: dict[str, Team]
) -> list[Tie]:
	"""
	Build the UEFA Nations League quarter-finals.

	The returned order defines the Final Four bracket:

		QF1 ─┐
			├── SF1
		QF2 ─┘

		QF3 ─┐
			├── SF2
		QF4 ─┘
	"""

	while True:
		ties = pair_rankings(
			seeded=winners,
			unseeded=runners_up,
			same_group_forbidden=True,
			teams = teams,
			iden = 0
			)
		if ties is not None:
			break

	for i, tie in enumerate(ties, start=1):
		if i%2==0:
			tie.name = f"QF{i-1} (Vuelta)"
		else:
			tie.name = f"QF{i} (Ida)   "

	return ties
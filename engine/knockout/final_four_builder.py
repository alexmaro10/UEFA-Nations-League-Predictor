from __future__ import annotations

from models.ranking import Ranking
from models.tie import Tie
from models.match import Match
from models.final_four import Final_Four

def build_final_four(
	ties: list[Tie],
	teams: dict[str, Team]
) -> list[Final_Four]:

	final_four = Final_Four(
		semi_final1= Match(
			id= 156+len(ties),
			phase="semi_final1",
			group = "",
			matchday = 9,
			home = ties[0].winner,
			away = ties[1].winner,
			played = False,
			home_goals = 0,
			away_goals = 0,
			winner = None,
			losser = None,
			local = False
		),
		semi_final2= Match(
			id= 156+len(ties),
			phase="semi_final2",
			group = "",
			matchday = 9,
			home = ties[2].winner,
			away = ties[3].winner,
			played = False,
			home_goals = 0,
			away_goals = 0,
			winner = None,
			losser = None,
			local = False
		)
	)
	return final_four
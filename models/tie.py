from __future__ import annotations

from dataclasses import dataclass, replace

from models.match import Match
from models.team import Team


@dataclass(slots=True)
class Tie:
	"""
	name: str
	home_team: Team
	away_team: Team
	home_goals: int
	away_goals: int
	first_leg: Match | None = None
	second_leg: Match | None = None
	winner: Team | None = None
	"""
	name: str
	first_match: Match
	second_match: Match
	first_leg: Match | None = None
	second_leg: Match | None = None
	winner: Team | None = None
	state: str | None = None
	def copy(self) -> "Tie":
		return replace(self)
	
	def to_dict(self) -> dict:
		return {
			"first_match": self.first_match.to_dict(),
			"second_match": self.second_match.to_dict(),
			"first_leg": self.first_leg.to_dict() if self.first_leg else None,
			"second_leg": self.second_leg.to_dict() if self.second_leg else None,
			"winner": self.winner.name if self.winner else None,
			"state": self.state
		}
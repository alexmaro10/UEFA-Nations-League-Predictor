from __future__ import annotations

from dataclasses import dataclass, replace
from models.team import Team

@dataclass(slots=True)
class Match:
	id: int
	phase: str
	group: str
	matchday: int
	home: str
	away: str
	played: bool
	home_goals: int
	away_goals: int
	winner: Team | None
	losser: Team | None
	local: bool

	def copy(self) -> "Match":
		return replace(self)
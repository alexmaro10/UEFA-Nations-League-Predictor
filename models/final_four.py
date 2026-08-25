from __future__ import annotations

from dataclasses import dataclass, replace

from models.match import Match

@dataclass(slots=True)
class Final_Four:
	semi_final1: Match
	semi_final2: Match
	third_place: Match  | None = None
	final: Match  | None = None
	winner_sf1: Team | None = None
	winner_sf2: Team | None = None
	losser_sf1: Team | None = None
	losser_sf2: Team | None = None
	winner_final: Team | None = None
	winner_third: Team | None = None
	losser_final: Team | None = None
	losser_third: Team | None = None
	def copy(self) -> "Tie":
		return replace(self)
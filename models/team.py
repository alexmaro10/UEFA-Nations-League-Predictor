from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class Team:
	id: int
	code: str
	name: str
	league: str
	group: str
	elo: float
	attack: float
	defense: float
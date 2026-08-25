from __future__ import annotations

from dataclasses import dataclass
from models.team import Team

@dataclass(slots=True)
class Standing:
	team: Team
	group: str
	position: int = 0
	played: int = 0
	wins: int = 0
	draws: int = 0
	losses: int = 0
	goals_for: int = 0
	goals_against: int = 0
	goal_difference: int = 0
	points: int = 0
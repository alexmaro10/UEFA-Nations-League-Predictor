from __future__ import annotations

from dataclasses import dataclass

from models.match import Match
from models.team import Team


@dataclass(slots=True)
class Group:
	"""
	Represents one UEFA Nations League group.
	"""

	name: str
	league: str

	teams: list[Team]
	matches: list[Match]
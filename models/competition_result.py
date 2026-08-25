from __future__ import annotations

from dataclasses import dataclass
from models.match import Match
from models.standing import Standing
from models.group import Group

@dataclass(slots=True)
class CompetitionResult:

	groups: dict[str, Group]
	standings: dict[str, list[Standing]]
	rankings: dict[str, Ranking]
from __future__ import annotations

from dataclasses import dataclass
from models.league import League
from models.group import Group

@dataclass(slots=True)
class Competition:
	leagues: list[League]
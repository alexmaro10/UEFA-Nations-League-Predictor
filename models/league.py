from __future__ import annotations

from dataclasses import dataclass
from models.group import Group

@dataclass(slots=True)
class League:
	name: str
	groups: list[Group]
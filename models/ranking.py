from __future__ import annotations

from dataclasses import dataclass

from models.standing import Standing

@dataclass(slots=True)
class Ranking:
	name: str
	standings: list[Standing]
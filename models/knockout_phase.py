from __future__ import annotations

from dataclasses import dataclass

from models.tie import Tie


@dataclass(slots=True)
class KnockoutPhase:
	quarter_finals: list[Tie]
	playoffs_ab: list[Tie]
	playoffs_bc: list[Tie]
	playoffs_cd: list[Tie]
	semi_finals: list[Tie]
	third_place: Tie | None
	final: Tie | None
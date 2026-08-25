from __future__ import annotations

from engine.builders.group_builder import build_groups
from engine.builders.league_builder import build_leagues

from models.competition import Competition
from models.match import Match

def build_competition(matches: list[Match]) -> Competition:
	groups = build_groups(matches)
	leagues = build_leagues(groups)

	return Competition(leagues = leagues)
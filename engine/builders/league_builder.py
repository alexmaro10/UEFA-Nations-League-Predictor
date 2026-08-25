from __future__ import annotations

from collections import defaultdict

from models.group import Group
from models.league import League


def build_leagues(groups: list[Group]) -> list[League]:
	grouped = defaultdict(list)
	
	for group in groups:
		grouped[group.league].append(group)
	
	leagues = []

	for league_name in sorted(grouped):
		leagues.append(
			League(
				name=league_name,
				groups=sorted(
					grouped[league_name],
					key=lambda g: g.name
				)
			)
		)

	return leagues
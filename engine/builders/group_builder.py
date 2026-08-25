from __future__ import annotations

from collections import defaultdict

from models.group import Group
from models.match import Match
from models.team import Team


def build_groups(matches: list[Match]) -> list[Group]:
	"""
	Build all competition groups from the fixture list.
	"""

	grouped_matches = defaultdict(list)

	for match in matches:
		grouped_matches[match.group].append(match)

	groups = []

	for group_name in sorted(grouped_matches):

		group_matches = grouped_matches[group_name]

		teams = {}

		for match in group_matches:
			teams[match.home.code] = match.home
			teams[match.away.code] = match.away

		groups.append(
			Group(
				name=group_name,
				league=group_name[0],
				teams=sorted(
					teams.values(),
					key=lambda t: t.code
				),
				matches=group_matches,
			)
		)

	return groups
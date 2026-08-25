from __future__ import annotations

from models.standing import Standing
from models.group import Group


def calculate_standings(group: Group) -> list[Standing]:

	standings: dict[str, Standing] = {}

	for match in group.matches:

		if match.home.code not in standings:
			standings[match.home.code] = Standing(
				team=match.home,
				group=group.name,
			)

		if match.away.code not in standings:
			standings[match.away.code] = Standing(
				team=match.away,
				group=group.name,
			)

	for match in group.matches:

		home = standings[match.home.code]
		away = standings[match.away.code]

		home.played += 1
		away.played += 1

		home.goals_for += match.home_goals
		home.goals_against += match.away_goals

		away.goals_for += match.away_goals
		away.goals_against += match.home_goals

		if match.home_goals > match.away_goals:

			home.wins += 1
			home.points += 3

			away.losses += 1

		elif match.home_goals < match.away_goals:

			away.wins += 1
			away.points += 3

			home.losses += 1

		else:

			home.draws += 1
			away.draws += 1

			home.points += 1
			away.points += 1

	for standing in standings.values():
		standing.goal_difference = (
			standing.goals_for - standing.goals_against
		)

	table = list(standings.values())

	table.sort(
		key=lambda s: (
			-s.points,
			-s.goal_difference,
			-s.goals_for,
		)
	)

	for position, standing in enumerate(table, start=1):
		standing.position = position

	return table
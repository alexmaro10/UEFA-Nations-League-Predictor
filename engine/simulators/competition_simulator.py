from __future__ import annotations

from engine.simulators.group_simulator import simulate_group
from engine.standings.standings_calculator import calculate_standings
from engine.rankings.ranking_builder import build_rankings
from models.competition import Competition
from models.competition_result import CompetitionResult
from models.group import Group
from models.standing import Standing

def simulate_competition(
	competition: Competition,
) -> CompetitionResult:
	"""
	Simulate the complete League Phase.
	"""

	simulated_groups: dict[str, Group] = {}

	standings: dict[str, list[Standing]] = {}

	for league in competition.leagues:

		for group in league.groups:

			simulated_group = simulate_group(group)

			simulated_groups[group.name] = simulated_group

			standings[group.name] = calculate_standings(simulated_group)

	rankings = build_rankings(standings)

	return CompetitionResult(
		groups=simulated_groups,
		standings=standings,
		rankings=rankings
	)
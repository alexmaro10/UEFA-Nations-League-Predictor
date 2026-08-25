from __future__ import annotations

from engine.simulators.match_simulator import simulate_match
from models.group import Group

def simulate_group(group: Group) -> Group:
	simulated_matches = []

	for match in group.matches:
		if match.played:
			simulated_matches.append(match.copy())
		else:
			simulated_matches.append(simulate_match(match))
	return Group(
		name = group.name,
		league = group.league,
		teams = group.teams,
		matches = simulated_matches
		)

from __future__ import annotations

from models.standing import Standing


def get_valid_opponents(
	standing: Standing,
	opponents: list[Standing],
	same_group_forbidden: bool = True,
) -> list[Standing]:

	valid_opponents: list[Standing] = []

	for opponent in opponents:

		if same_group_forbidden:

			if standing.group == opponent.group:
				continue

		valid_opponents.append(opponent)

	return valid_opponents
from __future__ import annotations

import json
from pathlib import Path

from models.match import Match
from models.team import Team


class MatchLoader:
	"""
	Loads fixtures from fixtures.json.
	"""
	@staticmethod
	def load(
		file_path: str | Path,
		teams: dict[str, Team]
	) -> list[Match]:

		file_path = Path(file_path)

		if not file_path.exists():
			raise FileNotFoundError(
				f"Fixtures file not found: {file_path}"
			)

		with file_path.open(
			mode="r",
			encoding="utf-8"
		) as f:

			data = json.load(f)

		matches: list[Match] = []

		ids: set[int] = set()

		for item in data["matches"]:

			match_id = item["id"]

			if match_id in ids:
				raise ValueError(
					f"Duplicate match id: {match_id}"
				)

			ids.add(match_id)

			home_code = item["home"]
			away_code = item["away"]

			if home_code not in teams:
				raise ValueError(
					f"Unknown home team '{home_code}' "
					f"in match {match_id}"
				)

			if away_code not in teams:
				raise ValueError(
					f"Unknown away team '{away_code}' "
					f"in match {match_id}"
				)

			matches.append(

				Match(

					id=match_id,

					phase=item["phase"],

					group=item["group"],

					matchday=item["matchday"],

					home=teams[home_code],

					away=teams[away_code],

					played=item["played"],

					home_goals=item["home_goals"],

					away_goals=item["away_goals"],

					winner=None,
					losser=None,
					local=True
				)

			)

		return matches
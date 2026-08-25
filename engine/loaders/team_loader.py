from __future__ import annotations

import csv
from pathlib import Path

from models.team import Team


class TeamLoader:
	"""
	Loads teams from elo.csv.
	"""

	@staticmethod
	def load(file_path: str | Path) -> tuple[dict[str, Team], dict[int, Team]]:
		file_path = Path(file_path)

		if not file_path.exists():
			raise FileNotFoundError(f"Teams file not found: {file_path}")

		teams_by_code: dict[str, Team] = {}
		teams_by_id: dict[int, Team] = {}

		with file_path.open(
			mode="r",
			encoding="utf-8",
			newline=""
		) as csvfile:

			reader = csv.DictReader(csvfile)

			for row in reader:

				team = Team(
					code=row["code"].strip(),
					name=row["name"].strip(),
					league=row["league"].strip(),
					group=row["group"].strip(),
					elo=float(row["elo"]),
					attack=float(row["attack_strength"]),
					defense=float(row["defense_strength"]),
					id=int(row["id"])
				)

				if team.code in teams_by_code:
					raise ValueError(
						f"Duplicate team code found: {team.code}"
					)

				if team.id in teams_by_id:
					raise ValueError(
						f"Duplicate team id found: {team.id}"
					)

				teams_by_code[team.code] = team
				teams_by_id[team.id] = team

		return teams_by_code, teams_by_id
import json
from pathlib import Path


def save_global_statistics(
	stats_league_a: list[list[int]],
	stats_league_b: list[list[int]],
	stats_league_c: list[list[int]],
	stats_league_d: list[list[int]],
	teams: dict,
) -> None:

	output_dir = Path("data/simulations")
	output_dir.mkdir(parents=True, exist_ok=True)

	file_path = output_dir / "statistics.json"

	data = {
		"league_A": build_league_a_statistics(stats_league_a, teams),
		"league_B": build_league_b_statistics(stats_league_b, teams),
		"league_C": build_league_c_statistics(stats_league_c, teams),
		"league_D": build_league_d_statistics(stats_league_d, teams),
	}

	with file_path.open("w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=2)


def build_league_a_statistics(
	stats: list[list[int]],
	teams: dict,
) -> list[dict]:

	result = []

	for row in stats:
		team_id = row[10]

		if team_id == 0 or team_id == 16:
			continue

		result.append({
			"team_id": team_id,
			"team_name": teams[team_id].name,

			"final_four": {
				"1": row[9],
				"2": row[8],
				"3": row[7],
				"4": row[6],
			},

			"relegated": row[4],

			"quarterfinal": row[2] + row[3] - row[9] - row[8] - row[7] - row[6],

			"group_position": {
				"4": row[0],
				"3": row[1],
				"2": row[2],
				"1": row[3],
			},
		})

	return result


def build_league_b_statistics(
	stats: list[list[int]],
	teams: dict,
) -> list[dict]:

	result = []

	for row in stats:
		team_id = row[6]

		if team_id == 0 or team_id == 16:
			continue

		result.append({
			"team_id": team_id,
			"team_name": teams[team_id].name,

			"group_position": {
				"4": row[0],
				"3": row[1],
				"2": row[2],
				"1": row[3],
			},

			"relegated": row[4],
			"promoted": row[5],
		})

	return result


def build_league_c_statistics(
	stats: list[list[int]],
	teams: dict,
) -> list[dict]:

	result = []

	for row in stats:
		team_id = row[6]

		if team_id == 0 or team_id == 16:
			continue

		result.append({
			"team_id": team_id,
			"team_name": teams[team_id].name,

			"group_position": {
				"4": row[0],
				"3": row[1],
				"2": row[2],
				"1": row[3],
			},

			"relegated": row[4],
			"promoted": row[5],
		})

	return result


def build_league_d_statistics(
	stats: list[list[int]],
	teams: dict,
) -> list[dict]:

	result = []

	for row in stats:
		team_id = row[4]

		if team_id == 0 or team_id == 16:
			continue

		result.append({
			"team_id": team_id,
			"team_name": teams[team_id].name,

			"group_position": {
				"3": row[0],
				"2": row[1],
				"1": row[2],
			},

			"promoted": row[3],
		})

	return result
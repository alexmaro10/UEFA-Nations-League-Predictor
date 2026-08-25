import json
from dataclasses import asdict
from pathlib import Path

from models.standing import Standing

def save_group_standings(
	simulation_id: int, 
	standings: list[Standing]) -> None:
	output_dir = Path("data/simulations")
	output_dir.mkdir(parents=True, exist_ok=True)

	file_path = output_dir / f"group_standings{simulation_id}.json"

	data = {
		"standings": [
			asdict(standing)
			for table in standings.values()
			for standing in table
		]
	}

	with file_path.open("w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=2)
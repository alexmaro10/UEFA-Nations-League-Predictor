import json
from dataclasses import asdict
from pathlib import Path

from models.match import Match


def save_simulation_matches(simulation_id: int, matches: list[Match]) -> None:
	output_dir = Path("data/simulations")
	output_dir.mkdir(parents=True, exist_ok=True)

	file_path = output_dir / f"matches_simulation_{simulation_id}.json"

	data = {
		"simulation_id": simulation_id,
		"matches": [asdict(match) for match in matches]
	}

	with file_path.open("w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=2)
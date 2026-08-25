import json
from pathlib import Path


def save_simulation_summaries(
	summaries: list[dict],
) -> None:

	output_dir = Path("data/simulations")
	output_dir.mkdir(parents=True, exist_ok=True)

	file_path = output_dir / "simulations.json"

	data = {
		"simulations": summaries
	}

	with file_path.open("w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=2)
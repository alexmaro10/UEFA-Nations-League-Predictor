from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(file_path: str | Path) -> dict[str, Any]:
	"""
	Load the application configuration from config.json.

	Args:
		file_path: Path to the configuration file.

	Returns:
		Dictionary containing the application configuration.

	Raises:
		FileNotFoundError: If the configuration file does not exist.
		ValueError: If the JSON is invalid.
	"""

	file_path = Path(file_path)

	if not file_path.exists():
		raise FileNotFoundError(f"Configuration file not found: {file_path}")

	try:
		with file_path.open("r", encoding="utf-8") as f:
			return json.load(f)

	except json.JSONDecodeError as e:
		raise ValueError(f"Invalid JSON in {file_path}: {e}")
import json
from pathlib import Path

from dataclasses import asdict
from engine.loaders.team_loader import TeamLoader
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/api")


SIMULATIONS_DIR = Path("data/simulations")


def load_json(filename: str):
	file_path = SIMULATIONS_DIR / filename

	if not file_path.exists():
		raise HTTPException(
			status_code=404,
			detail=f"No se encontró el archivo: {filename}"
		)

	try:
		with file_path.open("r", encoding="utf-8") as file:
			return json.load(file)

	except json.JSONDecodeError:
		raise HTTPException(
			status_code=500,
			detail=f"El archivo {filename} no contiene un JSON válido"
		)


@router.get("/results")
def get_results():
	statistics_path = SIMULATIONS_DIR / "statistics.json"
	simulations_path = SIMULATIONS_DIR / "simulations.json"

	if not statistics_path.exists() or not simulations_path.exists():
		return {
			"ready": False,
			"statistics": None,
			"simulations": None
		}

	statistics = load_json("statistics.json")
	simulations = load_json("simulations.json")

	return {
		"ready": True,
		"statistics": statistics,
		"simulations": simulations
	}

@router.post("/simulate")
def simulate():
	from main import run_simulations

	run_simulations()

	return {
		"success": True
	}

@router.get("/simulations/{simulation_id}")
def get_simulation(simulation_id: int):
	matches = load_json(f"matches_simulation_{simulation_id}.json")
	standings = load_json(f"group_standings{simulation_id}.json")

	return {
		"matches": matches,
		"standings": standings
	}

@router.get("/teams")
def get_teams():
	_, teams_by_id = TeamLoader.load("data/elo.csv")

	return {
		"teams": [asdict(team) for team in teams_by_id.values()]
	}
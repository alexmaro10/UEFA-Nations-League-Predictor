from __future__ import annotations
from models.team import Team

# Constantes calibradas contra ~4.500 partidos internacionales reales de los
# ultimos ~4 anios (ver data_prep/build_attack_defense.py y
# data_prep/output/model_params.json). Si vuelves a ejecutar ese script con
# datos actualizados, actualiza estos dos valores con los nuevos resultados.
BASE_GOALS = 1.246          # goles/equipo de media en campo neutral, fuerza media
HOME_ADVANTAGE = 1.329      # multiplicador de goles del local por jugar en casa


def calculate_expected_goals(
	home_team: Team,
	away_team: Team,
	local: bool
) -> tuple[float, float]:
	"""
	Calculate the expected goals (lambda) for both teams using ataque/defensa
	ratings ajustados a partir de resultados historicos reales (modelo tipo
	Dixon-Coles/Maher).

	home_team.attack / away_team.attack  -> por encima de 1 = ataque mejor que la media
	home_team.defense / away_team.defense -> por encima de 1 = encaja MAS que la media

	Returns:
		(home_lambda, away_lambda)
	"""

	if local:
		home_lambda = (
			BASE_GOALS
			* HOME_ADVANTAGE
			* home_team.attack
			* away_team.defense
		)

		away_lambda = (
			BASE_GOALS
			* away_team.attack
			* home_team.defense
		)
	else:
		home_lambda = (
			BASE_GOALS
			* home_team.attack
			* away_team.defense
		)
		away_lambda = (
			BASE_GOALS
			* away_team.attack
			* home_team.defense
		)
	return home_lambda, away_lambda



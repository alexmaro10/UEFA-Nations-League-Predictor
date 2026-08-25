"""
Calcula ratings de ataque y defensa por equipo a partir de resultados
historicos reales, usando un modelo de Poisson estilo Dixon-Coles/Maher:

    log(lambda_home) = mu + home_adv * es_local_de_verdad + attack[home] - defense[away]
    log(lambda_away) = mu +                                 attack[away] - defense[home]

- attack[t] alto  -> el equipo marca mas de lo esperado
- defense[t] alto -> el equipo ENCAJA MENOS de lo esperado (mejor defensa),
  porque se resta en la formula del rival. Para que el CSV de salida sea
  intuitivo (numero alto = "concede mas", igual que "attack alto = marca
  mas"), la columna exportada `defense_strength` es la INVERSA del
  parametro interno: exp(-defense[t]). No confundir una cosa con la otra.

Los partidos se ponderan por:
  - antiguedad (decaimiento exponencial, los partidos recientes pesan mas)
  - tipo de competicion (los amistosos pesan menos que los partidos oficiales)

Se aplica regularizacion ridge (L2) sobre attack/defense. Esto cumple dos
funciones a la vez:
  1) Resuelve la indeterminacion matematica del modelo (sin ella, se podria
     sumar una constante a todos los "attack" y restarla de mu sin cambiar
     la verosimilitud - el ridge selecciona automaticamente la solucion con
     attack/defense centrados en 0, que es la interpretacion natural de
     "por encima/por debajo de la media").
  2) Encoge las estimaciones de los equipos con pocos partidos (ej. San
     Marino, Gibraltar) hacia la media, evitando que un puñado de resultados
     extremos les asigne un rating disparatado.

Salida: data_prep/output/attack_defense.csv y model_params.json
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from team_mapping import OUR_NAME_TO_DATASET_NAME

# ----------------------------------------------------------------------
# Configuracion
# ----------------------------------------------------------------------

RESULTS_CSV = Path("../results_in_.csv")  # ajustar si mueves el CSV
ELO_CSV = Path("../data/elo.csv")
OUTPUT_DIR = Path("output")

HALF_LIFE_DAYS = 730          # un partido de hace 2 años pesa la mitad que uno de hoy
FRIENDLY_WEIGHT = 0.5         # peso relativo de los amistosos
RIDGE_ALPHA = 8.0             # fuerza de la regularizacion (mas alto = mas encogimiento)


# ----------------------------------------------------------------------
# Carga y limpieza
# ----------------------------------------------------------------------

def load_clean_matches(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Descarta filas mal formadas (sin equipo) o sin resultado (partidos aun no jugados)
    df = df.dropna(subset=["home_team", "away_team", "home_score", "away_score"]).copy()

    df["date"] = pd.to_datetime(df["date"])
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)
    df["neutral"] = df["neutral"].astype(bool)

    return df


def compute_weights(df: pd.DataFrame) -> np.ndarray:
    most_recent = df["date"].max()
    days_ago = (most_recent - df["date"]).dt.days.to_numpy()
    time_weight = 0.5 ** (days_ago / HALF_LIFE_DAYS)

    competition_weight = np.where(
        df["tournament"].str.contains("Friendly", case=False, na=False),
        FRIENDLY_WEIGHT,
        1.0,
    )

    return time_weight * competition_weight


# ----------------------------------------------------------------------
# Modelo
# ----------------------------------------------------------------------

def fit_attack_defense(df: pd.DataFrame, weights: np.ndarray):
    teams = sorted(set(df["home_team"]) | set(df["away_team"]))
    team_index = {name: i for i, name in enumerate(teams)}
    n_teams = len(teams)

    home_id = df["home_team"].map(team_index).to_numpy()
    away_id = df["away_team"].map(team_index).to_numpy()
    home_goals = df["home_score"].to_numpy(dtype=float)
    away_goals = df["away_score"].to_numpy(dtype=float)
    is_home_real = (~df["neutral"].to_numpy()).astype(float)  # 0 si neutral, 1 si de verdad local
    w = weights

    def unpack(params):
        mu = params[0]
        home_adv = params[1]
        attack = params[2 : 2 + n_teams]
        defense = params[2 + n_teams : 2 + 2 * n_teams]
        return mu, home_adv, attack, defense

    def neg_log_likelihood_and_grad(params):
        mu, home_adv, attack, defense = unpack(params)

        log_lambda_home = mu + home_adv * is_home_real + attack[home_id] - defense[away_id]
        log_lambda_away = mu + attack[away_id] - defense[home_id]

        lambda_home = np.exp(log_lambda_home)
        lambda_away = np.exp(log_lambda_away)

        # Log-verosimilitud de Poisson (se omiten los terminos log(y!), constantes)
        ll = w * (
            home_goals * log_lambda_home - lambda_home
            + away_goals * log_lambda_away - lambda_away
        )
        nll = -ll.sum() + RIDGE_ALPHA * (np.sum(attack ** 2) + np.sum(defense ** 2))

        # Gradiente analitico
        r_home = w * (lambda_home - home_goals)
        r_away = w * (lambda_away - away_goals)

        d_mu = (r_home + r_away).sum()
        d_home_adv = (r_home * is_home_real).sum()

        d_attack = (
            np.bincount(home_id, weights=r_home, minlength=n_teams)
            + np.bincount(away_id, weights=r_away, minlength=n_teams)
            + 2 * RIDGE_ALPHA * attack
        )
        d_defense = (
            -np.bincount(away_id, weights=r_home, minlength=n_teams)
            - np.bincount(home_id, weights=r_away, minlength=n_teams)
            + 2 * RIDGE_ALPHA * defense
        )

        grad = np.concatenate([[d_mu], [d_home_adv], d_attack, d_defense])
        return nll, grad

    x0 = np.zeros(2 + 2 * n_teams)
    x0[0] = np.log(df[["home_score", "away_score"]].to_numpy().mean())  # arranque razonable para mu

    result = minimize(
        neg_log_likelihood_and_grad,
        x0,
        jac=True,
        method="L-BFGS-B",
        options={"maxiter": 500},
    )

    if not result.success:
        print(f"AVISO: el optimizador no confirmo convergencia limpia: {result.message}")

    mu, home_adv, attack, defense = unpack(result.x)
    return teams, mu, home_adv, attack, defense


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    df = load_clean_matches(RESULTS_CSV)
    weights = compute_weights(df)

    print(f"Partidos usados tras limpieza: {len(df)}")
    print(f"Equipos distintos en el dataset global: {len(set(df['home_team']) | set(df['away_team']))}")

    teams, mu, home_adv, attack, defense = fit_attack_defense(df, weights)
    team_index = {name: i for i, name in enumerate(teams)}

    match_counts = pd.concat([df["home_team"], df["away_team"]]).value_counts()

    rows = []
    for our_name, dataset_name in OUR_NAME_TO_DATASET_NAME.items():
        if dataset_name not in team_index:
            print(f"AVISO: '{dataset_name}' ({our_name}) no aparece en el dataset, se omite")
            continue

        idx = team_index[dataset_name]
        rows.append(
            {
                "name": our_name,
                "attack": round(float(attack[idx]), 4),
                "defense": round(float(defense[idx]), 4),
                "attack_strength": round(float(np.exp(attack[idx])), 4),
                "defense_strength": round(float(np.exp(-defense[idx])), 4),
                "n_matches": int(match_counts.get(dataset_name, 0)),
            }
        )

    out_df = pd.DataFrame(rows).sort_values("attack", ascending=False)

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_df.to_csv(OUTPUT_DIR / "attack_defense.csv", index=False)

    with open(OUTPUT_DIR / "model_params.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "mu": float(mu),
                "home_advantage": float(home_adv),
                "ridge_alpha": RIDGE_ALPHA,
                "half_life_days": HALF_LIFE_DAYS,
                "friendly_weight": FRIENDLY_WEIGHT,
                "implied_avg_goals_neutral": float(np.exp(mu)),
                "implied_avg_goals_home_with_advantage": float(np.exp(mu + home_adv)),
            },
            f,
            indent=2,
        )

    print("\nTop 10 ataque:")
    print(out_df.sort_values("attack", ascending=False).head(10)[["name", "attack_strength", "n_matches"]].to_string(index=False))

    print("\nTop 10 mejor defensa (defense_strength mas bajo = encaja menos = mejor):")
    print(out_df.sort_values("defense_strength").head(10)[["name", "defense_strength", "n_matches"]].to_string(index=False))

    print("\nTop 10 peor defensa (defense_strength mas alto = encaja mas):")
    print(out_df.sort_values("defense_strength", ascending=False).head(10)[["name", "defense_strength", "n_matches"]].to_string(index=False))

    print(f"\nGoles/partido medios implicitos (campo neutral): {np.exp(mu):.2f}")
    print(f"Goles/partido medios implicitos (local con ventaja real): {np.exp(mu + home_adv):.2f}")
    print(f"\nGuardado en {OUTPUT_DIR}/attack_defense.csv y {OUTPUT_DIR}/model_params.json")


if __name__ == "__main__":
    main()

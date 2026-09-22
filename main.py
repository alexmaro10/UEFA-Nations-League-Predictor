from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.routes import router
from tqdm import tqdm

import glob
import os
import time
import json
import random

from output.simulation_storage import save_simulation_matches
from output.statistics_storage import save_global_statistics
from output.simulation_sumary import save_simulation_summaries
from output.groups_storage import save_group_standings

from engine.builders.competition_builder import build_competition

from engine.loaders.config_loader import load_config
from engine.loaders.match_loader import MatchLoader
from engine.loaders.team_loader import TeamLoader

from engine.simulators.competition_simulator import simulate_competition
from engine.simulators.tie_simulator import simulate_tie
from engine.simulators.semifinal_simulator import simulate_semifinals
from engine.simulators.finals_simulator import simulate_finals

from engine.knockout.quarterfinal_builder import build_quarter_finals
from engine.knockout.playoff_ab_builder import build_playoffs_ab
from engine.knockout.playoff_bc_builder import build_playoffs_bc
from engine.knockout.playoff_cd_builder import build_playoffs_cd
from engine.knockout.final_four_builder import build_final_four

from utils.prints import *

app = FastAPI(
	title="UEFA Nations League Predictor",
	version="1.0.0"
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(router)

N_SIMULATIONS = 100
N_SAVED_SIMULATIONS = 30

def clean_previous_simulations():
	simulations_dir = "data/simulations"

	patterns = [
		"matches_simulation_*.json",
		"group_standings*.json",
	]

	removed = 0
	for pattern in patterns:
		for file_path in glob.glob(os.path.join(simulations_dir, pattern)):
			os.remove(file_path)
			removed += 1

	if removed:
		print(f"✓ {removed} archivos de simulaciones anteriores eliminados")

def run_simulations():

	simulation_saved_ids = random.sample(range(1, N_SIMULATIONS + 1), N_SAVED_SIMULATIONS)
	print("=" * 60)
	print(f"UEF NATIONS LEAGUE SIMULATOR ({N_SIMULATIONS} simulations)")
	print("=" * 60)

	print("\nCleaning previous simulation files...")
	clean_previous_simulations()

	print("\nLoading configuration...")
	config = load_config("data/config.json")
	print("✓ Configuration loaded")

	print("\nLoading teams...")
	teams, teams_by_id = TeamLoader.load("data/elo.csv")
	print(f"✓ {len(teams)} teams loaded")

	print("\nLoading fixtures...")
	matches = MatchLoader.load("data/fixtures.json", teams)
	print(f"✓ {len(matches)} matches loaded")

	#[4fg, 3fg, 2fg, 1fg, Desc, CuartF, 4, 3, 2, 1, TeamID]
	stats_leagueA = [[0] * 11 for _ in range(56)]
	#[4fg, 3fg, 2fg, 1fg, Desc, Asc, TeamID]
	stats_leagueB = [[0] * 7 for _ in range(56)]
	#[4fg, 3fg, 2fg, 1fg, Desc, Asc, TeamID]
	stats_leagueC = [[0] * 7 for _ in range(56)]
	#[3fg, 2fg, 1fg, Asc, TeamID]
	stats_leagueD = [[0] * 5 for _ in range(56)]

	for i in range(1,56):
		stats_leagueA[i][10] = i
	for i in range(1,56):
		stats_leagueB[i][6] = i
	for i in range(1,56):
		stats_leagueC[i][6] = i
	for i in range(1,56):
		stats_leagueD[i][4] = i

	summaries = []

	print("")
	print("Simulating competition, please wait")
	for x in tqdm(range(1,N_SIMULATIONS+1)):
		#print("\nBuilding competition...")
		competition = build_competition(matches)
		#print("✓ Competition built")

		#print("\nSimulating competition...")
		result = simulate_competition(competition)
		#print("✓ Competition simulated")

		


		#print("\n")
		#print("=" * 60)
		#print("GROUP STANDINGS")
		#print("=" * 60)

		#for group_name in sorted(result.standings):
			#print_group(
				#result.groups[group_name],
				#result.standings[group_name]
			#)

		#print("\n")
		#print("=" * 60)
		#print("RANKINGS")
		#print("=" * 60)

		#for ranking_name in sorted(result.rankings):
			#print_ranking(result.rankings[ranking_name])

		#print("\n")
		#print("=" * 60)
		#print("KNOCKOUT DRAW")
		#print("=" * 60)

		quarter_finals = build_quarter_finals(
			result.rankings["A1"],
			result.rankings["A2"],
			teams
		)

		playoffs_ab = build_playoffs_ab(
			result.rankings["A3"],
			result.rankings["B2"],
			teams
		)

		playoffs_bc = build_playoffs_bc(
			result.rankings["B3"],
			result.rankings["C2"],
			teams
		)

		playoffs_cd = build_playoffs_cd(
			result.rankings["C4"],
			result.rankings["D2"],
			teams
		)

		for i in range(0,4):
			quarter_finals[i] = simulate_tie(quarter_finals[i])
			playoffs_ab[i] = simulate_tie(playoffs_ab[i])
			playoffs_bc[i] = simulate_tie(playoffs_bc[i])
		
		for i in range(0,2):
			playoffs_cd[i] = simulate_tie(playoffs_cd[i])
		
		#print_ties("Quarter-finals", quarter_finals)
		#print_ties("PlayOff A/B", playoffs_ab)
		#print_ties("PlayOff B/C", playoffs_bc)
		#print_ties("PlayOff C/D", playoffs_cd)

		final_four = build_final_four(quarter_finals, teams)
		
		final_four = simulate_semifinals(final_four)
		#print_semifinals(final_four)
		final_four = simulate_finals(final_four)
		#print_finals(final_four)

		"""print("\n" + "=" * 60)
		print("RESULTS")
		print("=" * 60)
		print(f"1. {final_four.winner_final.name}")
		print(f"2. {final_four.losser_final.name}")
		print(f"3. {final_four.winner_third.name}")
		print(f"4. {final_four.losser_third.name}")"""

		if x in simulation_saved_ids:
				all_matches = []
				for match in result.groups["A1"].matches:
					all_matches.append(match.copy())
				for match in result.groups["A2"].matches:
					all_matches.append(match.copy())
				for match in result.groups["A3"].matches:
					all_matches.append(match.copy())
				for match in result.groups["A4"].matches:
					all_matches.append(match.copy())
				for match in result.groups["B1"].matches:
					all_matches.append(match.copy())
				for match in result.groups["B2"].matches:
					all_matches.append(match.copy())
				for match in result.groups["B3"].matches:
					all_matches.append(match.copy())
				for match in result.groups["B4"].matches:
					all_matches.append(match.copy())
				for match in result.groups["C1"].matches:
					all_matches.append(match.copy())
				for match in result.groups["C2"].matches:
					all_matches.append(match.copy())
				for match in result.groups["C3"].matches:
					all_matches.append(match.copy())
				for match in result.groups["C4"].matches:
					all_matches.append(match.copy())
				for match in result.groups["D1"].matches:
					all_matches.append(match.copy())
				for match in result.groups["D2"].matches:
					all_matches.append(match.copy())
				
				for tie in quarter_finals:
					all_matches.append(tie.first_match.copy())
					all_matches.append(tie.second_match.copy())
				for tie in playoffs_ab:
					all_matches.append(tie.first_match.copy())
					all_matches.append(tie.second_match.copy())
				for tie in playoffs_bc:
					all_matches.append(tie.first_match.copy())
					all_matches.append(tie.second_match.copy())
				for tie in playoffs_cd:
					all_matches.append(tie.first_match.copy())
					all_matches.append(tie.second_match.copy())
				
				all_matches.append(final_four.semi_final1.copy())
				all_matches.append(final_four.semi_final2.copy())
				all_matches.append(final_four.third_place.copy())
				all_matches.append(final_four.final.copy())

				summaries.append({
					"simulation_id": x,
					"positions": {
						"1": final_four.winner_final.code,
						"2": final_four.losser_final.code,
						"3": final_four.winner_third.code,
						"4": final_four.losser_third.code
					}
				})

				save_simulation_summaries(summaries)

				save_simulation_matches(simulation_id=x, matches=all_matches)

				save_group_standings(simulation_id=x, standings=result.standings)




 ################# ESTADISTICAS FASE DE GRUPOS #########################

		for i in range(1,56):
			if i != 16:
				for j in range(0,4):
					if teams_by_id[i].id == result.rankings["A1"].standings[j].team.id:
						stats_leagueA[i][3] +=1
					if teams_by_id[i].id == result.rankings["A2"].standings[j].team.id:
						stats_leagueA[i][2] +=1
					if teams_by_id[i].id == result.rankings["A3"].standings[j].team.id:
						stats_leagueA[i][1] +=1
					if teams_by_id[i].id == result.rankings["A4"].standings[j].team.id:
						stats_leagueA[i][0] +=1
						stats_leagueA[i][4] +=1
					if teams_by_id[i].id == result.rankings["B1"].standings[j].team.id:
						stats_leagueB[i][3] +=1
						stats_leagueB[i][5] +=1
					if teams_by_id[i].id == result.rankings["B2"].standings[j].team.id:
						stats_leagueB[i][2] +=1
					if teams_by_id[i].id == result.rankings["B3"].standings[j].team.id:
						stats_leagueB[i][1] +=1
					if teams_by_id[i].id == result.rankings["B4"].standings[j].team.id:
						stats_leagueB[i][0] +=1
						stats_leagueB[i][4] +=1
					if teams_by_id[i].id == result.rankings["C1"].standings[j].team.id:
						stats_leagueC[i][3] +=1
						stats_leagueC[i][5] +=1
					if teams_by_id[i].id == result.rankings["C2"].standings[j].team.id:
						stats_leagueC[i][2] +=1
					if teams_by_id[i].id == result.rankings["C3"].standings[j].team.id:
						stats_leagueC[i][1] +=1
					if teams_by_id[i].id == result.rankings["C4"].standings[j].team.id:
						stats_leagueC[i][0] +=1
				for j in range(0,2):
					if teams_by_id[i].id == result.rankings["D1"].standings[j].team.id:
						stats_leagueD[i][2] +=1
						stats_leagueD[i][3] +=1
					if teams_by_id[i].id == result.rankings["D2"].standings[j].team.id:
						stats_leagueD[i][1] +=1
					if teams_by_id[i].id == result.rankings["D3"].standings[j].team.id:
						stats_leagueD[i][0] +=1

 #################### ESTADISTICAS DESCENSOS ############################

		for i in range(1,56):
			if i != 16:
				for j in range(0,4):
					if teams_by_id[i].id == result.rankings["A3"].standings[j].team.id:
						if int(playoffs_ab[0].winner.id) != i and int(playoffs_ab[1].winner.id) != i and int(playoffs_ab[2].winner.id) != i and int(playoffs_ab[3].winner.id) != i:
							stats_leagueA[i][4] += 1
					if teams_by_id[i].id == result.rankings["B3"].standings[j].team.id:
						if int(playoffs_bc[0].winner.id) != i and int(playoffs_bc[1].winner.id) != i and int(playoffs_bc[2].winner.id) != i and int(playoffs_bc[3].winner.id) != i:
							stats_leagueB[i][4] += 1
					if teams_by_id[i].id == result.rankings["C4"].standings[j].team.id:
						if j > 1:
							stats_leagueC[i][4] += 1
						elif int(playoffs_cd[0].winner.id) != i and int(playoffs_cd[1].winner.id) != i:
							stats_leagueC[i][4] += 1

 #################### ESTADISTICAS ASCENSOS ############################

		for i in range(1,56):
			if i != 16:
				for j in range(0,4):
					if teams_by_id[i].id == result.rankings["B2"].standings[j].team.id:
						if int(playoffs_ab[0].winner.id) == i or int(playoffs_ab[1].winner.id) == i or int(playoffs_ab[2].winner.id) == i or int(playoffs_ab[3].winner.id) == i:
							stats_leagueB[i][5] += 1
					if teams_by_id[i].id == result.rankings["C2"].standings[j].team.id:
						if int(playoffs_bc[0].winner.id) == i or int(playoffs_bc[1].winner.id) == i or int(playoffs_bc[2].winner.id) == i or int(playoffs_bc[3].winner.id) == i:
							stats_leagueC[i][5] += 1
					if j < 2:
						if teams_by_id[i].id == result.rankings["D2"].standings[j].team.id:
							if int(playoffs_cd[0].winner.id) == i or int(playoffs_cd[1].winner.id) == i:
								stats_leagueD[i][3] += 1
						
						
 ################## ESTADISTICAS FINAL_FOUR ############################
		for i in range(1,56):
			if int(final_four.winner_final.id) == i:
				stats_leagueA[i][9] +=1;
			elif int(final_four.losser_final.id) == i:
				stats_leagueA[i][8] +=1;
			elif int(final_four.winner_third.id) == i:
				stats_leagueA[i][7] +=1;
			elif int(final_four.losser_third.id) == i:
				stats_leagueA[i][6] +=1;


	print("\nGROUP A1")
	for team in result.groups["A1"].teams:
		print(f"{team.code} {stats_leagueA[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP A2")
	for team in result.groups["A2"].teams:
		print(f"{team.code} {stats_leagueA[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP A3")
	for team in result.groups["A3"].teams:
		print(f"{team.code} {stats_leagueA[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP A4")
	for team in result.groups["A4"].teams:
		print(f"{team.code} {stats_leagueA[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueA[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP B1")
	for team in result.groups["B1"].teams:
		print(f"{team.code} {stats_leagueB[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP B2")
	for team in result.groups["B2"].teams:
		print(f"{team.code} {stats_leagueB[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP B3")
	for team in result.groups["B3"].teams:
		print(f"{team.code} {stats_leagueB[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP B4")
	for team in result.groups["B4"].teams:
		print(f"{team.code} {stats_leagueB[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueB[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP C1")
	for team in result.groups["C1"].teams:
		print(f"{team.code} {stats_leagueC[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP C2")
	for team in result.groups["C2"].teams:
		print(f"{team.code} {stats_leagueC[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP C3")
	for team in result.groups["C3"].teams:
		print(f"{team.code} {stats_leagueC[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP C4")
	for team in result.groups["C4"].teams:
		print(f"{team.code} {stats_leagueC[team.id][3]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueC[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP D1")
	for team in result.groups["D1"].teams:
		print(f"{team.code} {stats_leagueD[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueD[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueD[team.id][0]/N_SIMULATIONS*100:.2f}%")
	print("\nGROUP D2")
	for team in result.groups["D2"].teams:
		print(f"{team.code} {stats_leagueD[team.id][2]/N_SIMULATIONS*100:.2f}% {stats_leagueD[team.id][1]/N_SIMULATIONS*100:.2f}% {stats_leagueD[team.id][0]/N_SIMULATIONS*100:.2f}%")

	print("\nASCENSOS")
	for i in range(1,56):
		if stats_leagueB[i][5] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueB[i][5]/N_SIMULATIONS*100:.2f}%")
		if stats_leagueC[i][5] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueC[i][5]/N_SIMULATIONS*100:.2f}%")
		if stats_leagueD[i][3] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueD[i][3]/N_SIMULATIONS*100:.2f}%")

	print("\nDESCENSOS")
	for i in range(1,56):
		if stats_leagueA[i][4] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueA[i][4]/N_SIMULATIONS*100:.2f}%")
		if stats_leagueB[i][4] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueB[i][4]/N_SIMULATIONS*100:.2f}%")
		if stats_leagueC[i][4] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueC[i][4]/N_SIMULATIONS*100:.2f}%")

	print("\nGANADORES: ")
	for i in range(1,56):
		if stats_leagueA[i][9] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueA[i][9]/N_SIMULATIONS*100:.2f}%")
	print("\nSEGUNDOS: ")
	for i in range(1,56):
		if stats_leagueA[i][8] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueA[i][8]/N_SIMULATIONS*100:.2f}%")
	print("\nTERCEROS: ")
	for i in range(1,56):
		if stats_leagueA[i][7] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueA[i][7]/N_SIMULATIONS*100:.2f}%")
	print("\nCUARTOS: ")
	for i in range(1,56):
		if stats_leagueA[i][6] > 0:
			print(f"{teams_by_id[i].name}: {stats_leagueA[i][6]/N_SIMULATIONS*100:.2f}%")
	
	save_global_statistics(stats_leagueA, stats_leagueB, stats_leagueC, stats_leagueD, teams_by_id)

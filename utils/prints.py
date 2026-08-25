from __future__ import annotations

def print_finals(final_four):

	print("\n" + "=" * 60)
	print("FINAL STAGE")
	print("=" * 60)

	print(
		f"FINAL"
		f"{final_four.final.home.code:>5}"
		f" {final_four.final.home_goals} - {final_four.final.away_goals} "
		f"{final_four.final.away.code:<5}\n"
		f"WINNER: {final_four.winner_final.code}"
		f"THIRD"
		f"{final_four.third_place.home.code:>5}"
		f" {final_four.third_place.home_goals} - {final_four.third_place.away_goals} "
		f"{final_four.third_place.away.code:<5}\n"
		f"WINNER: {final_four.winner_third.code}"
	)

def print_semifinals(final_four):

	print("\n" + "=" * 60)
	print("SEMIFINALS")
	print("=" * 60)

	print(
		f"SF1"
		f"{final_four.semi_final1.home.code:>5}"
		f" {final_four.semi_final1.home_goals} - {final_four.semi_final1.away_goals} "
		f"{final_four.semi_final1.away.code:<5}\n"
		f"Winner: {final_four.winner_sf1.code}\n"
		f"SF2"
		f"{final_four.semi_final2.home.code:>5}"
		f" {final_four.semi_final2.home_goals} - {final_four.semi_final2.away_goals} "
		f"{final_four.semi_final2.away.code:<5}\n"
		f"Winner: {final_four.winner_sf2.code}"
	)


def print_ties(title, ties):

	print("\n" + "=" * 60)
	print(title)
	print("=" * 60)

	for tie in ties:

		print(
			f"{tie.name:<4}"
			f"{tie.first_match.home.code:>5}"
			f" {tie.first_match.home_goals} - {tie.first_match.away_goals} "
			f"{tie.first_match.away.code:<5}"
			f"{tie.second_match.home.code:>5}"
			f" {tie.second_match.home_goals} - {tie.second_match.away_goals} "
			f"{tie.second_match.away.code:<5}"
		)
		if tie.state is None:
			print(f"Ganador: {tie.winner.code}")
		else:
			print(f"Ganador: {tie.winner.code} (p)")

def print_matches(group):

	print("\nMatches")

	current_matchday = None

	for match in sorted(group.matches, key=lambda m: (m.matchday, m.id)):

		if match.matchday != current_matchday:

			current_matchday = match.matchday

			print(f"\nMatchday {current_matchday}")

		print(
			f"{match.home.code:3} "
			f"{match.home_goals:>2} - {match.away_goals:<2} "
			f"{match.away.code:3}"
		)

def print_group(group, standings):

	print("\n" + "=" * 60)
	print(f"GROUP {group.name}")
	print("=" * 60)

	print_matches(group)

	print("\nStandings")

	print(
		f"{'Pos':<4}"
		f"{'Team':<5}"
		f"{'Pts':>5}"
		f"{'P':>5}"
		f"{'W':>5}"
		f"{'D':>5}"
		f"{'L':>5}"
		f"{'GF':>5}"
		f"{'GA':>5}"
		f"{'GD':>5}"
	)

	for pos, standing in enumerate(standings, start=1):

		print(
			f"{pos:<4}"
			f"{standing.team.code:<5}"
			f"{standing.points:>5}"
			f"{standing.played:>5}"
			f"{standing.wins:>5}"
			f"{standing.draws:>5}"
			f"{standing.losses:>5}"
			f"{standing.goals_for:>5}"
			f"{standing.goals_against:>5}"
			f"{standing.goal_difference:>5}"
		)


def print_ranking(ranking):

	print(f"\n===== RANKING {ranking.name} =====")

	print(
		f"{'Pos':<4}"
		f"{'Team':<5}"
		f"{'Group':<6}"
		f"{'Pts':>5}"
		f"{'GD':>5}"
		f"{'GF':>5}"
	)

	for pos, standing in enumerate(ranking.standings, start=1):

		print(
			f"{pos:<4}"
			f"{standing.team.code:<5}"
			f"{standing.team.group:<6}"
			f"{standing.points:>5}"
			f"{standing.goal_difference:>5}"
			f"{standing.goals_for:>5}"
		)

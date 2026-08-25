import { useState, useMemo } from 'react'
import LeagueTabs from './LeagueTabs'
import GroupStandingsTable from './GroupStandingsTable'
import MatchResults from './MatchResults'

function SimulationDetail({ simulationId, data, onClose }) {
	const [activeLeague, setActiveLeague] = useState('A')

	// Agrupa standings.standings por liga -> grupo (ordenados por posición)
	const standingsByLeague = useMemo(() => {
		const byLeague = {}

		for (const entry of data.standings.standings) {
		const league = entry.team.league
		const group = entry.group

		if (!byLeague[league]) byLeague[league] = {}
		if (!byLeague[league][group]) byLeague[league][group] = []

		byLeague[league][group].push(entry)
		}

		for (const league in byLeague) {
		for (const group in byLeague[league]) {
			byLeague[league][group].sort((a, b) => a.position - b.position)
		}
		}

		return byLeague
	}, [data])

	// Agrupa los partidos de fase de liga por liga -> grupo (ordenados por jornada)
	const matchesByLeague = useMemo(() => {
		const byLeague = {}

		for (const match of data.matches.matches) {
		if (match.phase !== 'league') continue

		const league = match.home.league
		const group = match.group

		if (!byLeague[league]) byLeague[league] = {}
		if (!byLeague[league][group]) byLeague[league][group] = []

		byLeague[league][group].push(match)
		}

		for (const league in byLeague) {
		for (const group in byLeague[league]) {
			byLeague[league][group].sort((a, b) => a.matchday - b.matchday)
		}
		}

		return byLeague
	}, [data])

	const matchesQuarterFinals = useMemo(() => {
		const quarterFinals = data.matches.matches.filter(match => match.phase === 'quarter-finals')
		quarterFinals.sort((a, b) => a.matchday - b.matchday)
		return quarterFinals
	}, [data])

	const matchesSemiFinals = useMemo(() => {
		const semiFinals = data.matches.matches.filter(match => match.phase === 'semi_final1' || match.phase === 'semi_final2')
		semiFinals.sort((a, b) => a.matchday - b.matchday)
		return semiFinals
	}, [data])

	const matchesFinals = useMemo(() => {
		const finals = data.matches.matches.filter(match => match.phase === 'final')
		finals.sort((a, b) => a.matchday - b.matchday)
		return finals
	}, [data])

	const matchesThirdPlace = useMemo(() => {
		const thirdPlace = data.matches.matches.filter(match => match.phase === 'thrid_place')
		thirdPlace.sort((a, b) => a.matchday - b.matchday)
		return thirdPlace
	}, [data])

	const matchesPlayoffsAB = useMemo(() => {
		const playoffsAB = data.matches.matches.filter(match => match.phase === 'playoffs ab')
		playoffsAB.sort((a, b) => a.matchday - b.matchday)
		return playoffsAB
	}, [data])

	const matchesPlayoffsBC = useMemo(() => {
		const playoffsBC = data.matches.matches.filter(match => match.phase === 'playoffs bc')
		playoffsBC.sort((a, b) => a.matchday - b.matchday)
		return playoffsBC
	}, [data])

	const matchesPlayoffsCD = useMemo(() => {
		const playoffsCD = data.matches.matches.filter(match => match.phase === 'playoffs cd')
		playoffsCD.sort((a, b) => a.matchday - b.matchday)
		return playoffsCD
	}, [data])

	const groupNames = Object.keys(standingsByLeague[activeLeague] || {}).sort()
	const showQuarterFinals = activeLeague === 'A' && matchesQuarterFinals.length > 0
	const showSemiFinals = activeLeague === 'A' && matchesSemiFinals.length > 0
	const showFinals = activeLeague === 'A' && matchesFinals.length > 0
	const showThirdPlace = activeLeague === 'A' && matchesThirdPlace.length > 0
	const showPlayoffsAB = (activeLeague === 'A' || activeLeague === 'B') && matchesPlayoffsAB.length > 0
	const showPlayoffsBC = (activeLeague === 'B' || activeLeague === 'C') && matchesPlayoffsBC.length > 0
	const showPlayoffsCD = (activeLeague === 'C' || activeLeague === 'D') && matchesPlayoffsCD.length > 0
	const hasKnockoutMatches = showQuarterFinals || showPlayoffsAB || showPlayoffsBC || showPlayoffsCD

	return (
		<div className="w-full max-w-4xl px-2 sm:px-3 lg:px-4">
		<div className="mb-5 flex items-center justify-between gap-3 border-b border-white/[0.07] pb-4">
			<div className="flex items-center gap-2.5">
				<span className="h-3.5 w-[3px] rounded-full bg-[linear-gradient(180deg,var(--color-blue),var(--color-cyan))]" />
				<div>
					<p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-cyan">SIMULACIÓN #{simulationId}</p>
					<h2 className="font-display text-[1.2rem] font-bold leading-tight text-ink sm:text-[1.35rem]">Detalle de la simulación</h2>
				</div>
			</div>
			<button
			onClick={onClose}
			className="rounded-md border border-white/[0.07] bg-navy-soft px-3 py-2 text-sm font-medium text-muted transition-colors hover:border-white/20 hover:text-ink"
			>
			Cerrar
			</button>
		</div>

		<LeagueTabs active={activeLeague} onChange={setActiveLeague} />

		<div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
			{groupNames.map((group) => (
			<div key={group}>
				<GroupStandingsTable
				group={group}
				teams={standingsByLeague[activeLeague][group]}
				/>
				<MatchResults matches={matchesByLeague[activeLeague]?.[group] || []} />
			</div>
			))}
		</div>

		{hasKnockoutMatches && (
			<div className="mt-8">
				<div className="mb-4 flex items-center gap-2">
					<span className="h-3 w-[3px] rounded-full bg-gold" />
					<span className="text-[11px] font-semibold uppercase tracking-widest text-muted-dim">
						Fase eliminatoria
					</span>
				</div>
				<div className="stripe-card grid grid-cols-1 gap-3 rounded-lg p-5 sm:p-6">
					{showPlayoffsAB && (
						<MatchResults matches={matchesPlayoffsAB} title="Playoff AB" />
					)}
					{showPlayoffsBC && (
						<MatchResults matches={matchesPlayoffsBC} title="Playoff BC" />
					)}
					{showPlayoffsCD && (
						<MatchResults matches={matchesPlayoffsCD} title="Playoff CD" />
					)}
					{showQuarterFinals && (
						<MatchResults matches={matchesQuarterFinals} title="Cuartos de final" />
					)}
					{showSemiFinals && (
						<MatchResults matches={matchesSemiFinals} title="Semifinales" />
					)}
					{showThirdPlace && (
						<MatchResults matches={matchesThirdPlace} title="Tercer puesto" />
					)}
					{showFinals && (
						<MatchResults matches={matchesFinals} title="Final" />
					)}
				</div>
			</div>
		)}
		</div>
	)
}

export default SimulationDetail

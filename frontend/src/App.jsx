import { useState, useMemo } from 'react'
import { runSimulation, getResults, getTeams, getSimulation } from './api/api'
import LeagueTabs from './components/LeagueTabs'
import LeaguePhaseTable from './components/LeaguePhaseTable'
import GroupPositionsSection from './components/GroupPositionsSection'
import SimulationCard from './components/SimulationCard'
import PaginationControls from './components/PaginationControls'
import SimulationDetail from './components/SimulationDetail'
import SectionHeader from './components/SectionHeader'

function App() {
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState(null)
	const [results, setResults] = useState(null)
	const [teams, setTeams] = useState(null)
	const [activeLeague, setActiveLeague] = useState('A')
	const [simulationsPage, setSimulationsPage] = useState(1)
	const SIMULATIONS_PER_PAGE = 12

	const [selectedSimulation, setSelectedSimulation] = useState(null)
	const [loadingSimulationId, setLoadingSimulationId] = useState(null)
	const [simulationError, setSimulationError] = useState(null)

	async function handleSimulate() {
		setLoading(true)
		setError(null)

		setSimulationsPage(1)
		try {
			await runSimulation()
			const [resultsData, teamsData] = await Promise.all([getResults(), getTeams()])
			setResults(resultsData)
			setTeams(teamsData.teams)
		} catch (err) {
			setError(err.message)
		} finally {
			setLoading(false)
		}
	}

	async function handleSelectSimulation(simulationId) {
		setLoadingSimulationId(simulationId)
		setSimulationError(null)

		try {
			const data = await getSimulation(simulationId)
			setSelectedSimulation({ id: simulationId, data })
		} catch (err) {
			setSimulationError(err.message)
		} finally {
			setLoadingSimulationId(null)
		}
	}

	const teamsById = useMemo(() => {
		if (!teams) return null
		const map = {}
		for (const team of teams) map[team.id] = team
		return map
	}, [teams])

	const teamsByCode = useMemo(() => {
		if (!teams) return null
		const map = {}
		for (const team of teams) map[team.code] = team
		return map
	}, [teams])

	const phaseStatsByLeague = useMemo(() => {
		if (!results?.statistics) return null

		const processLeague = (leagueKey, league) => {
			return results.statistics[leagueKey]
				.map((team) => {
					const total = Object.values(team.group_position).reduce((sum, v) => sum + v, 0)
					if (total === 0) return null

					const enriched = { ...team, total, code: teamsById[team.team_id]?.code }

					if (league === 'A') {
						const ff = team.final_four
						enriched.champion = ff['1']
						enriched.reachedFinal = ff['1'] + ff['2']
						enriched.reachedSemis = ff['1'] + ff['2'] + ff['3'] + ff['4']
						enriched.reachedQuarters = team.quarterfinal + enriched.reachedSemis
					}

					return enriched
				})
				.filter(Boolean)
		}

		const byLeague = {
			A: processLeague('league_A', 'A'),
			B: processLeague('league_B', 'B'),
			C: processLeague('league_C', 'C'),
			D: processLeague('league_D', 'D'),
		}

		byLeague.A.sort((a, b) => b.champion - a.champion)
		byLeague.B.sort((a, b) => b.promoted - a.promoted)
		byLeague.C.sort((a, b) => b.promoted - a.promoted)
		byLeague.D.sort((a, b) => b.promoted - a.promoted)

		return byLeague
	}, [results])

	const paginatedSimulations = useMemo(() => {
		if (!results?.simulations) return null

		const all = results.simulations.simulations
		const totalPages = Math.ceil(all.length / SIMULATIONS_PER_PAGE)
		const start = (simulationsPage - 1) * SIMULATIONS_PER_PAGE

		return {
			items: all.slice(start, start + SIMULATIONS_PER_PAGE),
			totalPages,
			total: all.length,
		}
	}, [results, simulationsPage])

	const groupPositionsByLeague = useMemo(() => {
		if (!results?.statistics || !teamsById) return null

		const buildGroups = (leagueKey) => {
			const groups = {}

			for (const team of results.statistics[leagueKey]) {
				const info = teamsById[team.team_id]
				if (!info) continue

				const total = Object.values(team.group_position).reduce((sum, v) => sum + v, 0)
				if (total === 0) continue

				const group = info.group
				if (!groups[group]) groups[group] = []

				groups[group].push({ ...team, total, code: info.code })
			}

			return groups
		}

		return {
			A: buildGroups('league_A'),
			B: buildGroups('league_B'),
			C: buildGroups('league_C'),
			D: buildGroups('league_D'),
		}
	}, [results, teamsById])

	return (
		<div className="relative min-h-screen overflow-hidden bg-navy font-body text-ink">
			<div className="pitch-grid absolute inset-0" />
			<div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_18%,_var(--color-navy-soft),_transparent_65%)]" />

			<div className="relative z-10 flex flex-col items-center">
				{/* BARRA SUPERIOR */}
				<header className="flex w-full max-w-6xl items-center justify-between px-4 py-6 sm:px-6 lg:px-8">
					<div className="flex items-center gap-2">
						<span className="h-2 w-2 rounded-full bg-cyan shadow-[0_0_8px_1px_var(--color-cyan)]" />
						<span className="font-display text-sm font-bold tracking-[0.08em] text-ink">
							UNL <span className="text-muted-dim">/</span> PREDICTOR
						</span>
					</div>
					<span
						className={`rounded-full border px-3 py-1 text-[10px] font-semibold tracking-widest ${
							results ? 'border-cyan/30 text-cyan' : 'border-white/10 text-muted-dim'
						}`}
					>
						{results ? 'DATOS CARGADOS' : 'SIN SIMULAR'}
					</span>
				</header>

				<div className="flex w-full flex-col items-center gap-16 px-4 pb-20 sm:px-6 lg:px-8">
					{/* HERO */}
					<div className="flex flex-col items-center pt-4 text-center max-w-2xl">
						<span className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-cyan">
							UEFA Nations League
						</span>

						<h1 className="mb-4 font-display text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
							Predictor
						</h1>

						<p className="mb-10 text-lg leading-relaxed text-muted sm:text-xl">
							Simulación Monte Carlo del torneo completo: 100.000 escenarios para anticipar quién levanta el trofeo.
						</p>

						<div className="relative">
							{!loading && (
								<>
									<span className="absolute inset-0 rounded-full border border-cyan/40 animate-pulse-ring" />
									<span className="absolute inset-0 rounded-full border border-cyan/40 animate-pulse-ring [animation-delay:0.8s]" />
								</>
							)}
							{!results && (
							<button
								onClick={handleSimulate}
								disabled={loading}
								className="relative rounded-full bg-[linear-gradient(90deg,var(--color-blue),var(--color-cyan))] px-10 py-4 font-display font-semibold tracking-wide text-navy shadow-[0_0_40px_-10px_var(--color-cyan)] transition-shadow hover:shadow-[0_0_55px_-8px_var(--color-cyan)] disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:shadow-[0_0_40px_-10px_var(--color-cyan)]"
							>
								{loading ? 'Simulando...' : 'Simular torneo'}
							</button>
							)}
						</div>

						{error && <p className="mt-4 text-sm text-danger">{error}</p>}

						<p className="mt-8 text-sm tracking-wide text-muted-dim">
							100.000 simulaciones · Liga A · B · C · D
						</p>
					</div>

					{/* ESTADÍSTICAS: fase final / movimientos + grupos */}
					{phaseStatsByLeague && groupPositionsByLeague && (
						<div className="w-full max-w-6xl">
							<SectionHeader
								eyebrow="Datos globales"
								title="Estadísticas por liga"
								trailing="100.000 SIMULACIONES"
							/>

							<LeagueTabs active={activeLeague} onChange={setActiveLeague} />

							<div className="mt-8">
								<LeaguePhaseTable league={activeLeague} teams={phaseStatsByLeague[activeLeague]} />
							</div>

							<div className="mt-12">
								<GroupPositionsSection league={activeLeague} groups={groupPositionsByLeague[activeLeague]} />
							</div>
						</div>
					)}

					{/* SIMULACIONES DESTACADAS */}
					{paginatedSimulations && teamsByCode && (
						<div className="w-full max-w-6xl">
							<SectionHeader
								eyebrow="Escenarios guardados"
								title="Simulaciones destacadas"
								trailing={`${paginatedSimulations.total} SELECCIONADAS`}
							/>

							<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
								{paginatedSimulations.items.map((sim) => (
									<SimulationCard
										key={sim.simulation_id}
										simulationId={sim.simulation_id}
										positions={sim.positions}
										teamsByCode={teamsByCode}
										onSelect={handleSelectSimulation}
										isLoading={loadingSimulationId === sim.simulation_id}
									/>
								))}
							</div>

							<PaginationControls
								currentPage={simulationsPage}
								totalPages={paginatedSimulations.totalPages}
								onPageChange={setSimulationsPage}
							/>

							{simulationError && (
								<p className="mt-4 text-sm text-danger">{simulationError}</p>
							)}
						</div>
					)}

					{/* DETALLE DE LA SIMULACIÓN SELECCIONADA */}
					{selectedSimulation && (
						<SimulationDetail
							simulationId={selectedSimulation.id}
							data={selectedSimulation.data}
							onClose={() => setSelectedSimulation(null)}
						/>
					)}
				</div>
			</div>
		</div>
	)
}

export default App
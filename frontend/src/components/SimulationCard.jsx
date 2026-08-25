import Flag from './Flag'

const MEDAL_STYLES = {
  1: 'text-gold',
  2: 'text-silver',
  3: 'text-bronze',
  4: 'text-muted-dim',
}

function SimulationCard({ simulationId, positions, teamsByCode, onSelect, isLoading }) {
  return (
    <div className="stripe-card flex flex-col rounded-lg p-5 sm:p-6">
      <p className="mb-3 text-[11px] font-semibold tracking-widest text-muted-dim">
        SIMULACIÓN #{simulationId}
      </p>

      <div className="mb-4 flex flex-col gap-1.5">
        {['1', '2', '3', '4'].map((pos) => {
          const code = positions[pos]
          const team = teamsByCode?.[code]

          return (
            <div key={pos} className="flex items-center gap-2 text-[15px]">
              <span className={`w-4 text-center tabular-nums text-sm font-bold ${MEDAL_STYLES[pos]}`}>
                {pos}
              </span>
              <Flag code={code} className="shrink-0" />
              <span className={pos === '1' ? 'font-medium text-ink' : 'text-muted'}>
                {team ? team.name : code}
              </span>
            </div>
          )
        })}
      </div>

      <button
        onClick={() => onSelect(simulationId)}
        disabled={isLoading}
        className="mt-auto w-full rounded-md border border-blue/60 py-2.5 font-display text-sm font-semibold text-cyan transition-colors hover:border-blue hover:bg-blue/10 disabled:opacity-50"
      >
        {isLoading ? 'Cargando...' : 'Ver simulación'}
      </button>
    </div>
  )
}

export default SimulationCard

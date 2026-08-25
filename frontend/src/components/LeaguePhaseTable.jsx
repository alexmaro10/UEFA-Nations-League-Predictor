import Flag from './Flag'

function formatPct(count, total) {
  if (!total) return '0.0%'
  return `${((count / total) * 100).toFixed(1)}%`
}

function LeaguePhaseTable({ league, teams }) {
  return (
    <div className="stripe-card w-full overflow-x-auto rounded-lg p-5 sm:p-6">
      <div className="mb-3 flex items-center gap-2">
        <span className="rounded-md bg-cyan px-2.5 py-1 font-display text-sm font-bold text-navy">
          LIGA {league}
        </span>
        <h4 className="text-base font-medium text-ink">
          {league === 'A' ? 'Fase final' : 'Movimientos de liga'}
        </h4>
      </div>

      <table className="w-full text-sm">
        <thead>
          <tr className="text-[11px] uppercase tracking-wide text-muted-dim">
            <th className="pb-2 text-left font-medium">Equipo</th>
            {league === 'A' && (
              <>
                <th className="pb-2 text-center font-medium">Descenso</th>
                <th className="pb-2 text-center font-medium">Cuartos</th>
                <th className="pb-2 text-center font-medium">Semis</th>
                <th className="pb-2 text-center font-medium">Final</th>
                <th className="pb-2 text-center font-medium">Campeón</th>
              </>
            )}
            {(league === 'B' || league === 'C') && (
              <>
                <th className="pb-2 text-center font-medium">Ascenso</th>
                <th className="pb-2 text-center font-medium">Descenso</th>
              </>
            )}
            {league === 'D' && <th className="pb-2 text-center font-medium">Ascenso</th>}
          </tr>
        </thead>
        <tbody>
          {teams.map((team, index) => (
            <tr
              key={team.team_id}
              className={`border-t border-white/[0.06] ${index % 2 === 1 ? 'bg-white/[0.015]' : ''}`}
            >
              <td className="py-2.5 font-medium text-ink whitespace-nowrap">
                <div className="flex items-center gap-1.5">
                  <Flag code={team.code} />
                  {team.team_name}
                </div>
              </td>

              {league === 'A' && (
                <>
                  <td className="py-2.5 text-center tabular-nums text-danger">
                    {formatPct(team.relegated, team.total)}
                  </td>
                  <td className="py-2.5 text-center tabular-nums text-muted">{formatPct(team.reachedQuarters, team.total)}</td>
                  <td className="py-2.5 text-center tabular-nums text-muted">{formatPct(team.reachedSemis, team.total)}</td>
                  <td className="py-2.5 text-center tabular-nums text-muted">{formatPct(team.reachedFinal, team.total)}</td>
                  <td className="py-2.5 text-center tabular-nums font-display font-bold text-gold">
                    {formatPct(team.champion, team.total)}
                  </td>
                </>
              )}

              {(league === 'B' || league === 'C') && (
                <>
                  <td className="py-2.5 text-center tabular-nums font-display font-bold text-cyan">
                    {formatPct(team.promoted, team.total)}
                  </td>
                  <td className="py-2.5 text-center tabular-nums text-danger">
                    {formatPct(team.relegated, team.total)}
                  </td>
                </>
              )}

              {league === 'D' && (
                <td className="py-2.5 text-center tabular-nums font-display font-bold text-cyan">
                  {formatPct(team.promoted, team.total)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default LeaguePhaseTable

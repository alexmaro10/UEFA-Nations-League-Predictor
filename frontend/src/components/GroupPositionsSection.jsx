import Flag from './Flag'

function formatPct(count, total) {
  if (!total) return '0.0%'
  return `${((count / total) * 100).toFixed(1)}%`
}

function GroupPositionsSection({ league, groups }) {
  const groupNames = Object.keys(groups).sort()
  const positions = league === 'D' ? ['1', '2', '3'] : ['1', '2', '3', '4']

  return (
    <div>
      <div className="mb-4 flex items-center gap-2">
        <span className="h-3 w-[3px] rounded-full bg-cyan" />
        <span className="text-[11px] font-semibold uppercase tracking-widest text-muted-dim">
          Probabilidad por posición de grupo
        </span>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
        {groupNames.map((group) => (
          <div key={group} className="stripe-card rounded-lg p-5 sm:p-6">
            <div className="mb-3 flex items-center gap-2">
              <span className="rounded-md bg-cyan px-2.5 py-1 font-display text-sm font-bold text-navy">
                {group}
              </span>
            </div>

            <table className="w-full text-sm">
              <thead>
                <tr className="text-[11px] uppercase tracking-wide text-muted-dim">
                  <th className="pb-2 text-left font-medium">Equipo</th>
                  {positions.map((pos) => (
                    <th key={pos} className="pb-2 text-center font-medium">{pos}º</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {groups[group].map((team, index) => (
                  <tr
                    key={team.team_id}
                    className={`border-t border-white/[0.06] ${index % 2 === 1 ? 'bg-white/[0.015]' : ''}`}
                  >
                    <td className="py-2.5 font-medium text-ink whitespace-nowrap">
                      <div className="flex items-center gap-1.5">
                        <Flag code={team.code} />
                        {team.code}
                      </div>
                    </td>
                    {positions.map((pos) => (
                      <td key={pos} className="py-2.5 text-center tabular-nums text-muted">
                        {formatPct(team.group_position[pos], team.total)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  )
}

export default GroupPositionsSection

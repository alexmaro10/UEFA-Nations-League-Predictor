import Flag from './Flag'

function GroupStandingsTable({ group, teams }) {
  return (
    <div className="stripe-card rounded-lg p-5 sm:p-6">
      <div className="mb-3 flex items-center gap-2">
        <span className="rounded-md bg-cyan px-2.5 py-1 font-display text-sm font-bold text-navy">
          {group}
        </span>
        <h4 className="text-base font-medium text-ink">Clasificación</h4>
      </div>

      <table className="w-full text-sm">
        <thead>
          <tr className="text-[11px] uppercase tracking-wide text-muted-dim">
            <th className="pb-2 text-left font-medium">#</th>
            <th className="pb-2 text-left font-medium">Equipo</th>
            <th className="pb-2 text-center font-medium">PJ</th>
            <th className="pb-2 text-center font-medium">G</th>
            <th className="pb-2 text-center font-medium">E</th>
            <th className="pb-2 text-center font-medium">P</th>
            <th className="pb-2 text-center font-medium">GF</th>
            <th className="pb-2 text-center font-medium">GC</th>
            <th className="pb-2 text-center font-medium">DG</th>
            <th className="pb-2 text-center font-medium">Pts</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((entry, index) => (
            <tr
              key={entry.team.id}
              className={`border-t border-white/[0.06] ${index % 2 === 1 ? 'bg-white/[0.015]' : ''}`}
            >
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.position}</td>
              <td className="py-2.5 font-medium text-ink">
                <div className="flex items-center gap-1.5">
                  <Flag code={entry.team.code} />
                  {entry.team.name}
                </div>
              </td>
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.played}</td>
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.wins}</td>
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.draws}</td>
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.losses}</td>
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.goals_for}</td>
              <td className="py-2.5 text-center tabular-nums text-muted">{entry.goals_against}</td>
              <td className="py-2.5 text-center tabular-nums text-muted">
                {entry.goal_difference > 0 ? `+${entry.goal_difference}` : entry.goal_difference}
              </td>
              <td className="py-2.5 text-center tabular-nums font-display font-bold text-cyan">
                {entry.points}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default GroupStandingsTable

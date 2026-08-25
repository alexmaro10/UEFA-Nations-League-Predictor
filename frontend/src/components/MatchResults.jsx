import Flag from './Flag'

function MatchResults({ matches, title = 'Resultados' }) {
  if (!matches?.length) return null

  // Agrupa los partidos (ya ordenados por matchday) en bloques por jornada
  const byMatchday = []
  let currentMatchday = null

  for (const match of matches) {
    if (match.matchday !== currentMatchday) {
      currentMatchday = match.matchday
      byMatchday.push({ matchday: match.matchday, matches: [] })
    }
    byMatchday[byMatchday.length - 1].matches.push(match)
  }

  return (
    <div className="mt-3 border-t border-dashed border-white/[0.08] pt-3">
      <p className="mb-2 text-[10px] font-semibold uppercase tracking-wide text-muted-dim">{title}</p>

      {byMatchday.map(({ matchday, matches: dayMatches }) => (
        <div key={matchday} className="mb-2 last:mb-0">
          <p className="mb-1.5 text-[10.5px] tabular-nums text-muted-dim">Jornada {matchday}</p>

          {dayMatches.map((match) => (
            <div
              key={`${match.matchday}-${match.home.code}-${match.away.code}`}
              className="mb-1 flex items-center justify-between rounded-md border border-white/[0.04] bg-white/[0.02] px-2.5 py-2 text-sm last:mb-0"
            >
              <span className="flex flex-1 items-center gap-1.5">
                <Flag code={match.home.code} />
                {match.home.name}
                {match.winner?.code === match.home.code && '*'}
              </span>
              <span className="px-3 tabular-nums font-display font-bold text-ink">
                {match.home_goals} – {match.away_goals}
              </span>
              <span className="flex flex-1 items-center justify-end gap-1.5 text-right">
                {match.winner?.code === match.away.code && '*'}
                {match.away.name}
                <Flag code={match.away.code} />
              </span>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

export default MatchResults

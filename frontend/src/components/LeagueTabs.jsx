const LEAGUES = ['A', 'B', 'C', 'D']

function LeagueTabs({ active, onChange }) {
  return (
    <div className="mx-auto flex w-fit gap-1 rounded-lg border border-white/[0.07] bg-navy-soft p-1">
      {LEAGUES.map((league) => (
        <button
          key={league}
          onClick={() => onChange(league)}
          className={`rounded-md px-6 py-2 font-display text-sm font-semibold tracking-wide transition-colors ${
            active === league
              ? 'bg-[linear-gradient(90deg,var(--color-blue),var(--color-cyan))] text-navy'
              : 'text-muted hover:text-ink'
          }`}
        >
          Liga {league}
        </button>
      ))}
    </div>
  )
}

export default LeagueTabs

function SectionHeader({ eyebrow, title, trailing }) {
  return (
    <div className="mb-6 flex items-end justify-between gap-4 border-b border-white/[0.07] pb-3">
      <div className="flex items-center gap-2.5">
        <span className="h-3.5 w-[3px] rounded-full bg-[linear-gradient(180deg,var(--color-blue),var(--color-cyan))]" />
        <div>
          {eyebrow && (
            <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-dim">
              {eyebrow}
            </p>
          )}
          {title && (
            <h2 className="font-display text-lg font-bold text-ink">{title}</h2>
          )}
        </div>
      </div>
      {trailing && (
        <span className="text-[10px] font-semibold tracking-[0.14em] text-cyan">
          {trailing}
        </span>
      )}
    </div>
  )
}

export default SectionHeader

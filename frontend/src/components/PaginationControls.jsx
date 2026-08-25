function PaginationControls({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null

  return (
    <div className="mt-6 flex items-center justify-center gap-3">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="rounded-md border border-white/[0.07] bg-navy-soft px-4 py-2 text-sm font-medium text-ink transition-colors hover:border-cyan/40 hover:text-cyan disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:border-white/[0.07] disabled:hover:text-ink"
      >
        Anterior
      </button>

      <span className="font-display text-sm tabular-nums text-muted">
        Página <span className="text-ink">{currentPage}</span> de {totalPages}
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="rounded-md border border-white/[0.07] bg-navy-soft px-4 py-2 text-sm font-medium text-ink transition-colors hover:border-cyan/40 hover:text-cyan disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:border-white/[0.07] disabled:hover:text-ink"
      >
        Siguiente
      </button>
    </div>
  )
}

export default PaginationControls

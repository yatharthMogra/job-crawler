export function CardSkeleton() {
  return (
    <div className="job-card-surface">
      <div className="flex min-h-[160px]">
        <div className="flex min-w-0 flex-1 gap-3 p-3.5 sm:p-4">
          <div className="size-11 shrink-0 animate-pulse rounded-lg bg-accent sm:size-[52px]" />
          <div className="flex min-w-0 flex-1 flex-col space-y-2">
            <div className="flex gap-1.5">
              <div className="h-4 w-14 animate-pulse rounded-full bg-secondary" />
              <div className="h-4 w-20 animate-pulse rounded-full bg-secondary" />
            </div>
            <div className="h-4 w-3/4 animate-pulse rounded bg-secondary" />
            <div className="h-3 w-1/2 animate-pulse rounded bg-secondary" />
            <div className="grid grid-cols-2 gap-2 pt-1 sm:grid-cols-3">
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
            </div>
            <div className="mt-auto flex items-center justify-between border-t border-border/50 pt-3">
              <div className="flex gap-3">
                <div className="h-3 w-20 animate-pulse rounded bg-secondary" />
                <div className="h-3 w-20 animate-pulse rounded bg-secondary" />
                <div className="h-3 w-16 animate-pulse rounded bg-secondary" />
              </div>
              <div className="flex gap-2">
                <div className="size-10 animate-pulse rounded-lg bg-secondary" />
                <div className="h-10 w-[88px] animate-pulse rounded-lg bg-secondary" />
              </div>
            </div>
          </div>
        </div>
        <div className="hidden w-[124px] shrink-0 animate-pulse border-l border-add/20 bg-add-muted/60 px-3.5 py-4 sm:block lg:w-[140px]">
          <div className="flex items-center gap-1.5">
            <div className="size-5 animate-pulse rounded-full bg-add/20" />
            <div className="h-2.5 w-16 animate-pulse rounded bg-add/20" />
          </div>
          <div className="mt-3 space-y-2">
            <div className="h-7 w-full animate-pulse rounded-lg border border-add/10 bg-white/60" />
            <div className="h-7 w-full animate-pulse rounded-lg border border-add/10 bg-white/60" />
            <div className="h-7 w-full animate-pulse rounded-lg border border-add/10 bg-white/60" />
          </div>
        </div>
        <div className="w-[108px] shrink-0 animate-pulse border-l border-border/40 bg-secondary/40 sm:w-[120px]" />
      </div>
    </div>
  )
}

export function FeedSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="flex flex-col gap-3">
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  )
}

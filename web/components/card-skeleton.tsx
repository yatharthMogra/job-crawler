export function CardSkeleton() {
  return (
    <div className="job-card-surface">
      <div className="flex">
        <div className="flex min-w-0 flex-1 gap-3 p-3.5 sm:p-4">
          <div className="size-11 shrink-0 animate-pulse rounded-lg bg-accent" />
          <div className="min-w-0 flex-1 space-y-2">
            <div className="flex gap-1.5">
              <div className="h-4 w-14 animate-pulse rounded-full bg-secondary" />
              <div className="h-4 w-20 animate-pulse rounded-full bg-secondary" />
            </div>
            <div className="h-4 w-3/4 animate-pulse rounded bg-secondary" />
            <div className="h-3 w-1/2 animate-pulse rounded bg-secondary" />
            <div className="grid grid-cols-3 gap-2 pt-1">
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
              <div className="h-3 animate-pulse rounded bg-secondary" />
            </div>
            <div className="flex items-center justify-between border-t border-border/50 pt-2">
              <div className="h-3 w-2/5 animate-pulse rounded bg-secondary" />
              <div className="flex gap-1.5">
                <div className="size-8 animate-pulse rounded-lg bg-secondary" />
                <div className="h-8 w-16 animate-pulse rounded-lg bg-secondary" />
              </div>
            </div>
          </div>
        </div>
        <div className="w-[76px] shrink-0 animate-pulse border-l border-border/40 bg-secondary/40 sm:w-[84px]" />
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

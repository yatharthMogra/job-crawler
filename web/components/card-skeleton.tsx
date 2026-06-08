export function CardSkeleton() {
  return (
    <div className="rounded-md border border-zinc-200 bg-white px-4 py-3">
      <div className="flex gap-4">
        <div className="flex flex-[3] gap-2.5">
          <div className="size-8 shrink-0 animate-pulse rounded-md bg-zinc-100" />
          <div className="flex-1 space-y-2">
            <div className="h-3.5 w-2/3 animate-pulse rounded bg-zinc-100" />
            <div className="h-3 w-1/2 animate-pulse rounded bg-zinc-100" />
            <div className="h-3 w-2/5 animate-pulse rounded bg-zinc-100" />
            <div className="mt-2 flex gap-1.5">
              <div className="h-7 w-16 animate-pulse rounded-md bg-zinc-100" />
              <div className="h-7 w-14 animate-pulse rounded-md bg-zinc-100" />
            </div>
          </div>
        </div>
        <div className="flex-[2] space-y-1.5 border-l border-zinc-100 pl-4">
          <div className="h-4 w-24 animate-pulse rounded-full bg-zinc-100" />
          <div className="h-4 w-20 animate-pulse rounded-full bg-zinc-100" />
          <div className="h-4 w-28 animate-pulse rounded-full bg-zinc-100" />
        </div>
      </div>
    </div>
  )
}

export function FeedSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="flex flex-col gap-2.5">
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  )
}

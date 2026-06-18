interface StatBlockProps {
  value: string
  label: string
}

export function StatBlock({ value, label }: StatBlockProps) {
  return (
    <div className="text-center">
      <p className="text-3xl font-bold text-primary sm:text-4xl">{value}</p>
      <p className="mt-1 text-sm font-medium text-muted-foreground">{label}</p>
    </div>
  )
}

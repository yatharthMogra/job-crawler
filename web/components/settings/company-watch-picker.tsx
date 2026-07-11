"use client"

import { useCallback, useEffect, useState } from "react"
import { X } from "lucide-react"
import { searchCompanies, type CompanySearchResult } from "@/lib/recommendation/api"
import { cn } from "@/lib/utils"

interface CompanyWatchPickerProps {
  selectedCompanyIds: string[]
  onChange: (companyIds: string[]) => void
  disabled?: boolean
  maxCompanies?: number
}

export function CompanyWatchPicker({
  selectedCompanyIds,
  onChange,
  disabled = false,
  maxCompanies = 5,
}: CompanyWatchPickerProps) {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<CompanySearchResult[]>([])
  const [selected, setSelected] = useState<CompanySearchResult[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (selectedCompanyIds.length === 0) {
      setSelected([])
      return
    }
    void searchCompanies("").then((companies) => {
      const map = new Map(companies.map((c) => [c.id, c]))
      setSelected(
        selectedCompanyIds
          .map((id) => map.get(id))
          .filter((c): c is CompanySearchResult => Boolean(c)),
      )
    })
  }, [selectedCompanyIds])

  useEffect(() => {
    if (disabled) return
    const handle = window.setTimeout(() => {
      setLoading(true)
      void searchCompanies(query)
        .then(setResults)
        .catch(() => setResults([]))
        .finally(() => setLoading(false))
    }, 300)
    return () => window.clearTimeout(handle)
  }, [query, disabled])

  const addCompany = useCallback(
    (company: CompanySearchResult) => {
      if (selectedCompanyIds.includes(company.id)) return
      if (selectedCompanyIds.length >= maxCompanies) return
      onChange([...selectedCompanyIds, company.id])
      setQuery("")
    },
    [onChange, selectedCompanyIds, maxCompanies],
  )

  const removeCompany = useCallback(
    (companyId: string) => {
      onChange(selectedCompanyIds.filter((id) => id !== companyId))
    },
    [onChange, selectedCompanyIds],
  )

  return (
    <div className="space-y-3">
      {selected.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {selected.map((company) => (
            <span
              key={company.id}
              className="inline-flex items-center gap-1 rounded-full border border-border bg-surface px-3 py-1 text-xs text-foreground"
            >
              {company.name}
              {!disabled ? (
                <button
                  type="button"
                  aria-label={`Remove ${company.name}`}
                  onClick={() => removeCompany(company.id)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <X className="size-3" />
                </button>
              ) : null}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">No companies watched yet.</p>
      )}
      {!disabled && selectedCompanyIds.length >= maxCompanies ? (
        <p className="text-xs text-muted-foreground">
                      You&apos;ve reached your plan limit of {maxCompanies} companies. Upgrade to Plus
                      ($4.99/month, 25 companies) or Pro ($19.99/month, 100 companies) in Settings.
        </p>
      ) : null}

      {!disabled ? (
        <>
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search company catalog…"
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-foreground"
          />
          {loading ? <p className="text-xs text-muted-foreground">Searching…</p> : null}
          {results.length > 0 && query.trim() ? (
            <ul className="max-h-40 overflow-y-auto rounded-lg border border-border bg-surface">
              {results
                .filter((c) => !selectedCompanyIds.includes(c.id))
                .slice(0, 8)
                .map((company) => (
                  <li key={company.id}>
                    <button
                      type="button"
                      onClick={() => addCompany(company)}
                      className={cn(
                        "flex w-full items-center justify-between px-3 py-2 text-left text-sm",
                        "hover:bg-accent/50",
                      )}
                    >
                      <span>{company.name}</span>
                      <span className="text-xs text-muted-foreground">{company.platform}</span>
                    </button>
                  </li>
                ))}
            </ul>
          ) : null}
          <p className="text-xs text-muted-foreground">
            Can&apos;t find a company?{" "}
            <a href="mailto:support@careermatch.ai?subject=Company%20catalog%20request" className="text-brand hover:underline">
              Request it be added
            </a>
          </p>
        </>
      ) : null}
    </div>
  )
}

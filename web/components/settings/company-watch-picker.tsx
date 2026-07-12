"use client"

import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { Plus, Search, X } from "lucide-react"
import { CompanyLogo } from "@/components/company-logo"
import { searchCompanies, type CompanySearchResult } from "@/lib/recommendation/api"
import { cn } from "@/lib/utils"

interface CompanyWatchPickerProps {
  selectedCompanyIds: string[]
  onChange: (companyIds: string[]) => void
  disabled?: boolean
  maxCompanies?: number
  /** Optional hydrated watch rows (includes logo_url when API provides it). */
  knownCompanies?: Array<{
    company_id: string
    company_name: string
    platform: string
    logo_url?: string | null
  }>
}

function SlotMeter({ used, max }: { used: number; max: number }) {
  const remaining = Math.max(0, max - used)
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3 text-xs">
        <span className="font-medium text-foreground">
          {used === 0
            ? `Add up to ${max} companies`
            : remaining > 0
              ? `${remaining} slot${remaining === 1 ? "" : "s"} left`
              : "All slots filled"}
        </span>
        <span className="tabular-nums text-muted-foreground">
          {used}/{max}
        </span>
      </div>
      <div className="flex gap-1.5" aria-hidden="true">
        {Array.from({ length: Math.min(max, 10) }, (_, i) => (
          <div
            key={i}
            className={cn(
              "h-1.5 flex-1 rounded-full transition-colors duration-300",
              i < used ? "bg-primary" : "bg-muted",
            )}
          />
        ))}
        {max > 10 ? (
          <div
            className={cn(
              "h-1.5 min-w-8 flex-[2] rounded-full transition-colors duration-300",
              used >= max ? "bg-primary" : "bg-muted",
            )}
          />
        ) : null}
      </div>
    </div>
  )
}

export function CompanyWatchPicker({
  selectedCompanyIds,
  onChange,
  disabled = false,
  maxCompanies = 5,
  knownCompanies = [],
}: CompanyWatchPickerProps) {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<CompanySearchResult[]>([])
  const [suggestions, setSuggestions] = useState<CompanySearchResult[]>([])
  const [selected, setSelected] = useState<CompanySearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [focused, setFocused] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const atLimit = selectedCompanyIds.length >= maxCompanies
  const remaining = Math.max(0, maxCompanies - selectedCompanyIds.length)

  useEffect(() => {
    if (selectedCompanyIds.length === 0) {
      setSelected([])
      return
    }

    const knownMap = new Map(
      knownCompanies.map((c) => [
        c.company_id,
        {
          id: c.company_id,
          name: c.company_name,
          platform: c.platform,
          is_active: true,
          logo_url: c.logo_url ?? null,
        } satisfies CompanySearchResult,
      ]),
    )

    void searchCompanies("").then((companies) => {
      const searchMap = new Map(companies.map((c) => [c.id, c]))
      setSelected(
        selectedCompanyIds.map((id) => {
          const known = knownMap.get(id)
          const fromSearch = searchMap.get(id)
          if (known && fromSearch) {
            return {
              ...fromSearch,
              logo_url: known.logo_url ?? fromSearch.logo_url ?? null,
            }
          }
          return (
            known ??
            fromSearch ?? {
              id,
              name: "Company",
              platform: "",
              is_active: true,
              logo_url: null,
            }
          )
        }),
      )
    })
  }, [selectedCompanyIds, knownCompanies])

  useEffect(() => {
    if (disabled) return
    void searchCompanies("")
      .then((companies) => setSuggestions(companies.slice(0, 12)))
      .catch(() => setSuggestions([]))
  }, [disabled])

  useEffect(() => {
    if (disabled || !query.trim()) {
      setResults([])
      return
    }
    const handle = window.setTimeout(() => {
      setLoading(true)
      void searchCompanies(query)
        .then(setResults)
        .catch(() => setResults([]))
        .finally(() => setLoading(false))
    }, 250)
    return () => window.clearTimeout(handle)
  }, [query, disabled])

  const addCompany = useCallback(
    (company: CompanySearchResult) => {
      if (selectedCompanyIds.includes(company.id)) return
      if (selectedCompanyIds.length >= maxCompanies) return
      onChange([...selectedCompanyIds, company.id])
      setQuery("")
      setFocused(false)
    },
    [onChange, selectedCompanyIds, maxCompanies],
  )

  const removeCompany = useCallback(
    (companyId: string) => {
      onChange(selectedCompanyIds.filter((id) => id !== companyId))
    },
    [onChange, selectedCompanyIds],
  )

  const suggestionPool = useMemo(
    () =>
      suggestions
        .filter((c) => !selectedCompanyIds.includes(c.id))
        .slice(0, remaining > 0 ? Math.min(6, remaining + 2) : 0),
    [suggestions, selectedCompanyIds, remaining],
  )

  const searchHits = useMemo(
    () => results.filter((c) => !selectedCompanyIds.includes(c.id)).slice(0, 8),
    [results, selectedCompanyIds],
  )

  return (
    <div className="space-y-4">
      <SlotMeter used={selectedCompanyIds.length} max={maxCompanies} />

      {selected.length > 0 ? (
        <ul className="grid gap-2 sm:grid-cols-2">
          {selected.map((company, index) => (
            <li
              key={company.id}
              className="flex items-center gap-3 rounded-xl border border-border/80 bg-card px-3 py-2.5 shadow-sm transition-transform duration-300 hover:-translate-y-0.5"
              style={{ animationDelay: `${index * 40}ms` }}
            >
              <CompanyLogo
                company={company.name}
                size={40}
                shape="square"
                logoUrl={company.logo_url}
              />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-foreground">{company.name}</p>
                <p className="truncate text-[11px] uppercase tracking-wide text-muted-foreground">
                  {company.platform || "Watched"}
                </p>
              </div>
              {!disabled ? (
                <button
                  type="button"
                  aria-label={`Remove ${company.name}`}
                  onClick={() => removeCompany(company.id)}
                  className="rounded-full p-1.5 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                >
                  <X className="size-3.5" />
                </button>
              ) : null}
            </li>
          ))}
        </ul>
      ) : (
        <div className="rounded-xl border border-dashed border-primary/30 bg-gradient-to-br from-primary/[0.06] to-transparent px-4 py-5 text-center">
          <div className="mx-auto mb-3 flex justify-center -space-x-2">
            {["Stripe", "Notion", "Figma", "Anthropic"].map((name) => (
              <CompanyLogo key={name} company={name} size={36} shape="circle" className="ring-2 ring-card" />
            ))}
          </div>
          <p className="text-sm font-semibold text-foreground">Start with companies you care about</p>
          <p className="mt-1 text-sm text-muted-foreground">
            Free includes {maxCompanies} watches. Search below or tap a logo — we&apos;ll email you when they
            post matching roles.
          </p>
          {!disabled ? (
            <button
              type="button"
              onClick={() => inputRef.current?.focus()}
              className="btn-brand mt-4 inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold"
            >
              <Search className="size-4" />
              Search companies
            </button>
          ) : null}
        </div>
      )}

      {!disabled && atLimit ? (
        <p className="rounded-lg border border-border/70 bg-muted/40 px-3 py-2 text-xs text-muted-foreground">
          You&apos;ve used all {maxCompanies} slots. Remove one to add another, or upgrade in Settings for Plus
          (25) or Pro (100).
        </p>
      ) : null}

      {!disabled && !atLimit ? (
        <div className="space-y-3">
          <div
            className={cn(
              "flex items-center gap-2 rounded-xl border bg-card px-3 py-2.5 shadow-sm transition-shadow",
              focused ? "border-primary/50 ring-2 ring-primary/15" : "border-border/80",
            )}
          >
            <Search className="size-4 shrink-0 text-muted-foreground" />
            <input
              ref={inputRef}
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => window.setTimeout(() => setFocused(false), 150)}
              placeholder="Type a company name to add…"
              className="w-full bg-transparent text-sm text-foreground outline-none placeholder:text-muted-foreground"
              aria-label="Search companies to watch"
            />
            {loading ? <span className="text-[11px] text-muted-foreground">Searching…</span> : null}
          </div>

          {query.trim() && searchHits.length > 0 ? (
            <ul className="max-h-56 overflow-y-auto rounded-xl border border-border/80 bg-card shadow-md">
              {searchHits.map((company) => (
                <li key={company.id} className="border-b border-border/50 last:border-0">
                  <button
                    type="button"
                    onMouseDown={(e) => e.preventDefault()}
                    onClick={() => addCompany(company)}
                    className="flex w-full items-center gap-3 px-3 py-2.5 text-left text-sm transition-colors hover:bg-accent/60"
                  >
                    <CompanyLogo
                      company={company.name}
                      size={32}
                      shape="square"
                      logoUrl={company.logo_url}
                    />
                    <span className="min-w-0 flex-1 truncate font-medium text-foreground">
                      {company.name}
                    </span>
                    <span className="inline-flex items-center gap-1 text-xs font-semibold text-primary">
                      <Plus className="size-3.5" />
                      Add
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          ) : null}

          {query.trim() && !loading && searchHits.length === 0 ? (
            <p className="text-xs text-muted-foreground">
              No matches.{" "}
              <a
                href="mailto:support@careermatch.ai?subject=Company%20catalog%20request"
                className="font-medium text-brand hover:underline"
              >
                Request this company
              </a>
            </p>
          ) : null}

          {!query.trim() && suggestionPool.length > 0 ? (
            <div className="space-y-2">
              <p className="text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">
                Quick add
              </p>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                {suggestionPool.map((company) => (
                  <button
                    key={company.id}
                    type="button"
                    onClick={() => addCompany(company)}
                    className="flex items-center gap-2.5 rounded-xl border border-border/80 bg-card px-2.5 py-2 text-left shadow-sm transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:bg-primary/5"
                  >
                    <CompanyLogo
                      company={company.name}
                      size={32}
                      shape="square"
                      logoUrl={company.logo_url}
                    />
                    <span className="min-w-0 flex-1">
                      <span className="block truncate text-xs font-semibold text-foreground">
                        {company.name}
                      </span>
                      <span className="text-[10px] font-medium text-primary">+ Add</span>
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ) : null}

          <p className="text-xs text-muted-foreground">
            Can&apos;t find a company?{" "}
            <a
              href="mailto:support@careermatch.ai?subject=Company%20catalog%20request"
              className="font-medium text-brand hover:underline"
            >
              Request it be added
            </a>
          </p>
        </div>
      ) : null}
    </div>
  )
}

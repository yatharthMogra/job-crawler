function key(candidateId: string, kind: "saved" | "applied" | "hidden") {
  return `cma_${kind}_${candidateId}`
}

function readIds(candidateId: string, kind: "saved" | "applied" | "hidden"): Set<string> {
  if (typeof window === "undefined") return new Set()
  try {
    const raw = localStorage.getItem(key(candidateId, kind))
    if (!raw) return new Set()
    const parsed = JSON.parse(raw) as string[]
    return new Set(parsed)
  } catch {
    return new Set()
  }
}

function writeIds(candidateId: string, kind: "saved" | "applied" | "hidden", ids: Set<string>) {
  localStorage.setItem(key(candidateId, kind), JSON.stringify([...ids]))
}

export function loadSavedIds(candidateId: string) {
  return readIds(candidateId, "saved")
}

export function loadAppliedIds(candidateId: string) {
  return readIds(candidateId, "applied")
}

export function loadHiddenIds(candidateId: string) {
  return readIds(candidateId, "hidden")
}

export function persistSavedIds(candidateId: string, ids: Set<string>) {
  writeIds(candidateId, "saved", ids)
}

export function persistAppliedIds(candidateId: string, ids: Set<string>) {
  writeIds(candidateId, "applied", ids)
}

export function persistHiddenIds(candidateId: string, ids: Set<string>) {
  writeIds(candidateId, "hidden", ids)
}

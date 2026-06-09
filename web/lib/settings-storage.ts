export interface JobAlertsSettings {
  instantEnabled: boolean
  instantFrequency: "1" | "unlimited"
  digestEnabled: boolean
  digestFrequency: "daily" | "weekly"
}

const DEFAULT_ALERTS: JobAlertsSettings = {
  instantEnabled: true,
  instantFrequency: "1",
  digestEnabled: true,
  digestFrequency: "daily",
}

function key(candidateId: string, kind: "job_alerts") {
  return `cma_${kind}_${candidateId}`
}

export function loadJobAlertsSettings(candidateId: string): JobAlertsSettings {
  if (typeof window === "undefined") return DEFAULT_ALERTS
  try {
    const raw = localStorage.getItem(key(candidateId, "job_alerts"))
    if (!raw) return DEFAULT_ALERTS
    return { ...DEFAULT_ALERTS, ...JSON.parse(raw) }
  } catch {
    return DEFAULT_ALERTS
  }
}

export function persistJobAlertsSettings(candidateId: string, settings: JobAlertsSettings) {
  localStorage.setItem(key(candidateId, "job_alerts"), JSON.stringify(settings))
}

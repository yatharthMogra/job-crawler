"use client"

import { useEffect, useState } from "react"

export function useCountUp(
  target: number,
  active: boolean,
  duration = 1400,
  decimals = 0,
) {
  const [value, setValue] = useState(0)

  useEffect(() => {
    if (!active) return

    let frame = 0
    const start = performance.now()

    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - (1 - progress) ** 3
      setValue(target * eased)
      if (progress < 1) frame = requestAnimationFrame(tick)
    }

    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [target, active, duration])

  return decimals > 0 ? value.toFixed(decimals) : Math.round(value).toLocaleString()
}

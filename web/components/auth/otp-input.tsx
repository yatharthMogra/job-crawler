"use client"

import { useRef } from "react"
import { cn } from "@/lib/utils"

interface OtpInputProps {
  value: string
  onChange: (value: string) => void
  disabled?: boolean
  className?: string
}

export function OtpInput({ value, onChange, disabled, className }: OtpInputProps) {
  const inputsRef = useRef<Array<HTMLInputElement | null>>([])

  const digits = Array.from({ length: 6 }, (_, index) => value[index] ?? "")

  function updateDigit(index: number, digit: string) {
    const next = digits.slice()
    next[index] = digit
    onChange(next.join("").slice(0, 6))
  }

  function handleChange(index: number, raw: string) {
    const digit = raw.replace(/\D/g, "").slice(-1)
    updateDigit(index, digit)
    if (digit && index < 5) {
      inputsRef.current[index + 1]?.focus()
    }
  }

  function handleKeyDown(index: number, key: string) {
    if (key === "Backspace" && !digits[index] && index > 0) {
      inputsRef.current[index - 1]?.focus()
    }
  }

  function handlePaste(event: React.ClipboardEvent<HTMLInputElement>) {
    event.preventDefault()
    const pasted = event.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6)
    if (!pasted) return
    onChange(pasted)
    const focusIndex = Math.min(pasted.length, 5)
    inputsRef.current[focusIndex]?.focus()
  }

  return (
    <div className={cn("flex items-center justify-center gap-2", className)}>
      {digits.map((digit, index) => (
        <input
          key={index}
          ref={(element) => {
            inputsRef.current[index] = element
          }}
          type="text"
          inputMode="numeric"
          autoComplete={index === 0 ? "one-time-code" : "off"}
          maxLength={1}
          value={digit}
          disabled={disabled}
          onChange={(event) => handleChange(index, event.target.value)}
          onKeyDown={(event) => handleKeyDown(index, event.key)}
          onPaste={handlePaste}
          className="h-12 w-10 rounded-xl border border-border/80 bg-surface/50 text-center text-lg font-semibold text-foreground outline-none transition-colors focus:border-primary focus:ring-2 focus:ring-primary/20 disabled:opacity-50"
          aria-label={`Digit ${index + 1}`}
        />
      ))}
    </div>
  )
}

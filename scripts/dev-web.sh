#!/usr/bin/env bash
set -eo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/web"

if [[ ! -f .env.local && -f .env.example ]]; then
  echo "No .env.local found — copy .env.example and set NEXT_PUBLIC_PROFILE_API_KEY"
fi

ensure_node_on_path() {
  if command -v npm >/dev/null 2>&1; then
    return 0
  fi

  # nvm — disable nounset while sourcing (nvm.sh uses unset vars)
  local nvm_dir="${NVM_DIR:-${HOME:-}/.nvm}"
  if [[ -s "${nvm_dir}/nvm.sh" ]]; then
    set +u
    # shellcheck source=/dev/null
    . "${nvm_dir}/nvm.sh"
    set -u 2>/dev/null || true
    command -v npm >/dev/null 2>&1 && return 0
  fi

  # nvm without sourcing: pick latest installed node version
  if [[ -d "${nvm_dir}/versions/node" ]]; then
    local latest
    latest="$(ls "${nvm_dir}/versions/node" 2>/dev/null | sort -V | tail -1)"
    if [[ -n "${latest}" && -x "${nvm_dir}/versions/node/${latest}/bin/npm" ]]; then
      export PATH="${nvm_dir}/versions/node/${latest}/bin:${PATH}"
      command -v npm >/dev/null 2>&1 && return 0
    fi
  fi

  # Homebrew / system installs
  for dir in /opt/homebrew/bin /usr/local/bin; do
    if [[ -x "${dir}/npm" ]]; then
      export PATH="${dir}:${PATH}"
      return 0
    fi
  done

  return 1
}

if ! ensure_node_on_path; then
  echo "Could not find npm on PATH." >&2
  echo "Install Node.js: https://nodejs.org or run: nvm install --lts" >&2
  exit 1
fi

# Prefer Node 22 (more stable with Next.js than Node 24)
if [[ -d "${HOME}/.nvm/versions/node/v22.23.1/bin" ]]; then
  export PATH="${HOME}/.nvm/versions/node/v22.23.1/bin:${PATH}"
fi

PORT="${PORT:-3001}"
export PORT

echo ""
echo "  Starting Job Scout frontend..."
echo "  Open → http://127.0.0.1:${PORT}"
echo "  (First start can take 1–2 min — wait for 'Ready')"
echo ""

if command -v pnpm >/dev/null 2>&1; then
  exec pnpm dev
fi

exec npm run dev

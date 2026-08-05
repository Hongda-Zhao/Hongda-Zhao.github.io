#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
LOCAL_QUARTO="${PROJECT_DIR}/../.tools/quarto-1.10.18/bin/quarto"

if command -v quarto >/dev/null 2>&1; then
  QUARTO_BIN="$(command -v quarto)"
elif [[ -x "${LOCAL_QUARTO}" ]]; then
  QUARTO_BIN="${LOCAL_QUARTO}"
else
  echo "Quarto was not found. Install it from https://quarto.org/docs/get-started/" >&2
  exit 1
fi

cd "${PROJECT_DIR}"
exec "${QUARTO_BIN}" render "$@"

#!/usr/bin/env bash
set -euo pipefail

# Find the repository root, including paths containing spaces.
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Prefer the project's environment. Allow an explicit Python path.
PYTHON_BIN="${PYTHON_BIN:-$PROJECT_ROOT/.venv/bin/python}"

if [[ ! -x "$PYTHON_BIN" ]]; then
    echo "Python environment not found."
    echo "Create .venv or set PYTHON_BIN to your environment's Python."
    exit 1
fi

echo "Checking the Ganache connection..."
"$PYTHON_BIN" scripts/check_connection.py

echo "Starting a new demonstration..."
"$PYTHON_BIN" scripts/deploy_contract.py
"$PYTHON_BIN" scripts/fund_contract.py
"$PYTHON_BIN" scripts/buy_policy.py
"$PYTHON_BIN" scripts/report_delay.py
"$PYTHON_BIN" scripts/claim_compensation.py

echo "Demonstration completed successfully."
#!/usr/bin/env bash
# Full verification pass: fixtures -> mirror -> page -> comparison.
set -euo pipefail
cd "$(dirname "$0")"
[ -d node_modules ] || npm install --no-audit --no-fund
python3 fixtures/make_fixtures.py
python3 mirror.py > /dev/null
node run.mjs
python3 compare.py

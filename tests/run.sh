#!/usr/bin/env bash
# Full verification pass: RU freshness -> fixtures -> mirror -> page -> comparison.
set -euo pipefail
cd "$(dirname "$0")"
[ -d node_modules ] || npm install --no-audit --no-fund

# The RU page is GENERATED from the EN one. If someone edits the EN page and forgets
# to run the build script - or the build script itself breaks - the RU page silently
# goes stale and every RU assertion below keeps passing against yesterday's file.
# So: regenerate it and require the result to be byte-identical to what is on disk.
RU=../tools/seasonality/ru/index.html
cp "$RU" .out-ru-committed.html 2>/dev/null || mkdir -p .out && cp "$RU" .out-ru-committed.html
if ! python3 ../build/build_ru_page.py > .out-ru-build.log 2>&1; then
  echo "FAIL  RU build script errored:"; sed 's/^/      /' .out-ru-build.log; exit 1
fi
if ! diff -q .out-ru-committed.html "$RU" > /dev/null; then
  echo "FAIL  RU page is stale - regenerating it changed the file."
  echo "      The EN page was edited without running build/build_ru_page.py."
  diff .out-ru-committed.html "$RU" | head -20 | sed 's/^/      /'
  cp .out-ru-committed.html "$RU"        # leave the tree as we found it
  rm -f .out-ru-committed.html .out-ru-build.log
  exit 1
fi
grep -q 'leftover suspects: none' .out-ru-build.log || {
  echo "FAIL  RU page has leftover English:"; grep 'leftover' .out-ru-build.log | sed 's/^/      /'; exit 1; }
echo "PASS  RU page is freshly generated from the EN page, no leftover English"
rm -f .out-ru-committed.html .out-ru-build.log

python3 fixtures/make_fixtures.py
python3 mirror.py > /dev/null
node run.mjs
python3 compare.py

#!/usr/bin/env bash
set -euo pipefail

reports_dir="${REPORTS_DIR:-reports}"
mkdir -p "$reports_dir" test-results

python -m pytest tests/ \
  -n auto \
  --junitxml="$reports_dir/junit.xml" \
  --html="$reports_dir/report.html" \
  --self-contained-html \
  --tracing=retain-on-failure \
  --screenshot=only-on-failure \
  --video=retain-on-failure \
  --output=test-results

#!/usr/bin/env bash
set -euo pipefail

# Check if pdm is installed, if not install it
command -v pdm >/dev/null 2>&1 || pip install pdm
pdm install
python -m mypy .
python -m pytest -vv

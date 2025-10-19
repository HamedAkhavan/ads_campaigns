#!/usr/bin/env bash
set -euo pipefail

pdm install
python -m mypy .
python -m pytest -vv

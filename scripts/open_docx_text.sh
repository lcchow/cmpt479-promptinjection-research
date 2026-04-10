#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "usage: open_docx_text.sh <path-to-docx>" >&2
  exit 2
fi
DOCX_PATH="$1"
if [ ! -f "$DOCX_PATH" ]; then
  echo "ERROR: file not found: $DOCX_PATH" >&2
  exit 3
fi
python3 /home/var/.openclaw/workspace/openclaw_security_research_faithful/scripts/extract_docx_text.py "$DOCX_PATH"

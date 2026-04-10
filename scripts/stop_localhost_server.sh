#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/var/.openclaw/workspace/openclaw_security_research"
PID_FILE="$ROOT/results/http_server.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No PID file present"
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "Stopped HTTP server PID $PID"
else
  echo "PID $PID not running"
fi
rm -f "$PID_FILE"

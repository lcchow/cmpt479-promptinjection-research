#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/var/.openclaw/workspace/openclaw_security_research"
ARTIFACTS_DIR="$ROOT/artifacts"
PORT="${1:-8080}"
PID_FILE="$ROOT/results/http_server.pid"
LOG_FILE="$ROOT/results/http_server.log"

mkdir -p "$ROOT/results"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "HTTP server already running on PID $(cat "$PID_FILE")"
  exit 0
fi

nohup python3 -m http.server "$PORT" --directory "$ARTIFACTS_DIR" >"$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "Started HTTP server on http://127.0.0.1:$PORT/ serving $ARTIFACTS_DIR (PID $(cat "$PID_FILE"))"

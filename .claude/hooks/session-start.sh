#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$(dirname "$(dirname "$0")")")}"

echo "[session-start] Installing Python dependencies..."
pip install -r requirements.txt --quiet

echo "[session-start] Done."

# Sync Eclectic Polymath episodes from Spotify (auto if credentials set, reminder otherwise)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/sync-eclectic-episodes.py" 2>/dev/null || true

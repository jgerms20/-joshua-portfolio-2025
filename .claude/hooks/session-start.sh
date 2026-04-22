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

# Check Eclectic Polymath for new episodes (prints reminder if it's been 5+ days)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/check-eclectic-episodes.py" 2>/dev/null || true

#!/usr/bin/env python3
"""
Checks The Eclectic Polymath Podcast for episode count drift.
Runs at session start to remind Joshua to add new episodes to the portfolio.
"""
import json
import re
import os
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).parent.parent.parent))
PODCAST_HTML = PROJECT_DIR / "podcasts" / "podcast-eclectic-polymath.html"
TRACKER_FILE = PROJECT_DIR / ".claude" / "eclectic-podcast-tracker.json"
SPOTIFY_SHOW_URL = "https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069"
CHECK_INTERVAL_DAYS = 5  # Remind every 5 days


def count_episodes_in_html() -> int:
    if not PODCAST_HTML.exists():
        return 0
    content = PODCAST_HTML.read_text()
    # Count Spotify episode embeds
    return len(re.findall(r'open\.spotify\.com/embed/episode/', content))


def load_tracker() -> dict:
    if TRACKER_FILE.exists():
        try:
            return json.loads(TRACKER_FILE.read_text())
        except Exception:
            pass
    return {"last_checked": None, "last_known_count": 0}


def save_tracker(data: dict):
    TRACKER_FILE.write_text(json.dumps(data, indent=2))


def main():
    current_count = count_episodes_in_html()
    tracker = load_tracker()
    last_checked = tracker.get("last_checked")
    last_known_count = tracker.get("last_known_count", 0)

    now = datetime.now()

    # Update tracker if episode count changed
    if current_count != last_known_count:
        print(f"\n🎙️  [Eclectic Polymath] Portfolio updated: {last_known_count} → {current_count} episodes.")
        tracker["last_known_count"] = current_count
        tracker["last_checked"] = now.isoformat()
        save_tracker(tracker)
        return

    # Check if it's been a while since we last reminded
    should_remind = True
    if last_checked:
        try:
            last_dt = datetime.fromisoformat(last_checked)
            days_since = (now - last_dt).days
            should_remind = days_since >= CHECK_INTERVAL_DAYS
        except Exception:
            pass

    if should_remind:
        print(f"\n🎙️  [Eclectic Polymath] You have {current_count} episodes in the portfolio.")
        print(f"   Check Spotify for new episodes: {SPOTIFY_SHOW_URL}")
        print(f"   If you've added one, run: /add-eclectic-episode")
        tracker["last_checked"] = now.isoformat()
        save_tracker(tracker)


if __name__ == "__main__":
    main()

# Sync Episodes — The Eclectic Polymath Podcast

Checks Spotify for new Eclectic Polymath episodes and adds any missing ones to the portfolio automatically.

## How it works

1. Calls the Spotify API using your credentials
2. Compares Spotify's episode list against what's already in `podcasts/podcast-eclectic-polymath.html`
3. Inserts any new episodes at the top (newest first), updates the episode count badge
4. Commits and pushes automatically

## Run it now

```bash
python3 .claude/hooks/sync-eclectic-episodes.py
```

## One-time setup (required for auto mode)

Without credentials the script falls back to a 5-day reminder. To enable full auto-sync:

1. Go to https://developer.spotify.com/dashboard
2. Log in → **Create app** → give it any name/description → check "Web API" → Save
3. In the app → **Settings** → copy **Client ID** and **Client Secret**
4. Add to Claude Code settings (`.claude/settings.json` or user settings):

```json
{
  "env": {
    "SPOTIFY_CLIENT_ID": "your_client_id_here",
    "SPOTIFY_CLIENT_SECRET": "your_client_secret_here"
  }
}
```

Or export them in your shell before running:
```bash
export SPOTIFY_CLIENT_ID=your_id
export SPOTIFY_CLIENT_SECRET=your_secret
python3 .claude/hooks/sync-eclectic-episodes.py
```

## What runs automatically

- **Session start**: `sync-eclectic-episodes.py` runs every time a Claude Code web session starts
- **Loop**: `/loop` re-runs this sync every 6 hours in the background

## Show info

- Spotify show ID: `3dlagzJ0jiWLTB9mF3y069`
- Show URL: https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069
- Portfolio page: `podcasts/podcast-eclectic-polymath.html`

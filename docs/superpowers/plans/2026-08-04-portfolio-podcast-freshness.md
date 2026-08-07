# Portfolio Podcast Freshness Plan

**Goal:** Keep The Eclectic Polymath page honest and prove its live Spotify catalog is advancing.

## Implementation

- [x] Add recorded-fixture tests for parsing Spotify's newest episode marker, title, link, and date label.
- [x] Fail live health checks if the feed regresses below the verified episode baseline.
- [x] Fail live health checks if the newest release becomes older than the permitted freshness window.
- [x] Remove hard-coded `56` and `99` episode counts from the public page.
- [x] Replace them with live-catalog language that matches the self-updating Spotify embed.
- [x] Run the probe from the existing read-only Monday/Friday GitHub Actions schedule.
- [x] Verify focused tests and the real Spotify page.

The tracked baseline is episode 106 as observed on August 4, 2026. A newer episode passes automatically; the repository does not need a count-only commit for each release.

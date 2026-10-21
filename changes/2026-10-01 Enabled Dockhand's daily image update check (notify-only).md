---
date: 2026-10-01
type: fix
system:
- '[[Dockhand]]'
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3ec7ae76-22ba-8160-b92a-d771ec3633c0
---

# Enabled Dockhand's daily image update check (notify-only)

The Big Boi environment's update check was disabled, so Dockhand never flagged updates. Enabled it via dockhand-api (Aaron approved): daily 0 4 * * *, autoUpdate off. A manual check then flagged all 7 servarr containers ([lscr.io](http://lscr.io/), [ghcr.io](http://ghcr.io/) and Docker Hub all work).

**Cause:** `GET /api/environments/1/update-check` returned `enabled: false` (cron `0 4 * * *` preset), and no update-check job existed in `/api/schedules`. Registry access was never the problem.
**Change (approved by Aaron in chat; first write through ****`dockhand-api --write`****, after Aaron added the Claude Code allow rule for it):**
- `POST /api/environments/1/update-check` `{enabled: true, cron: "0 4 * * *", autoUpdate: false, vulnerabilityCriteria: "never"}`.
- `POST /api/containers/check-updates?env=1`: a one-off check (job), done within ~5 s.
**Result 2026-10-01 18:38 UTC:** `hasImageUpdate: true` for gluetun (`qmcgaw/gluetun`), gluetun-watchdog (`alpine:latest`), nzbget, prowlarr, radarr, sonarr (`lscr.io/linuxserver/*:latest`), seerr (`ghcr.io/seerr-team/seerr:latest`). Not flagged: uptime-kuma (`:2`), Dockhand (`v1.0.49`), ix-dockhand helper. Nothing was pulled or restarted.
**Not yet configured:** the global "Newer version tags" setting (Settings → General), which only matters for pinned tags.

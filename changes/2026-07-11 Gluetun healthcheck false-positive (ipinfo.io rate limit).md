---
date: 2026-07-11
type: fix
system:
- '[[Servarr Stack (Docker Compose)]]'
notion_id: 39a7ae76-22ba-8111-80e2-cb8f57d98744
---

# Gluetun healthcheck false-positive (ipinfo.io rate limit) — caused NZBGet/Prowlarr restart loop

Separate root cause from the IP-race bug fixed earlier today. Gluetun's Docker healthcheck was configured as `wget -q -O /dev/null https://ipinfo.io || exit 1` — hitting a free third-party 'what's my IP' API every 30 seconds, continuously, for hours. [ipinfo.io](http://ipinfo.io/) began returning 429 Too Many Requests to the shared ProtonVPN exit IP (confirmed by running the exact command manually: `docker exec gluetun wget -O- https://ipinfo.io` returned HTTP 429). This made Gluetun's Docker health status flip to 'unhealthy' continuously (FailingStreak reached 946) even though the VPN tunnel and actual downloads were completely fine. gluetun-watchdog reads Gluetun's health via `docker inspect --format='{{.State.Health.Status}}' gluetun` over the mounted Docker socket (confirmed via its entrypoint script) and restarted nzbget+prowlarr every ~37 seconds as a result — this is what caused NZBGet's WebUI to show 'Communication error' repeatedly (the container was actually being stopped/restarted, not just losing a browser connection; downloads continued seamlessly across each restart since NZBGet resumes cleanly). Fix: changed the healthcheck target to Gluetun's own internal health server, `http://127.0.0.1:9999`, which is purpose-built for this and immune to external rate limits. Edited directly in the live compose file (/mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/servarr/compose.yaml, line ~35), backed up first. Recreated Gluetun alone (sequenced: stopped nzbget/prowlarr/gluetun-watchdog first, recreated gluetun, confirmed Health=healthy, then restarted the other three). Verified fixed: FailingStreak reset to 0, and gluetun-watchdog's restart loop stopped entirely — last false restart at 18:59:02 UTC, confirmed clean through 19:09:48 UTC (10+ minutes, ~20 check cycles) with no recurrence.

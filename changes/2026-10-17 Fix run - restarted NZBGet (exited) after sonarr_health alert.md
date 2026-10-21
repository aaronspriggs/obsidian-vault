---
date: 2026-10-17
type: fix
system:
- '[[Servarr Stack (Docker Compose)]]'
notion_id: 3fc7ae76-22ba-81a2-9a0a-ebc0f9991d3c
---

# Fix run: restarted NZBGet (exited) after sonarr_health alert

Alert sonarr_health: Sonarr reported 'Unable to communicate with NZBGet, connection refused (172.39.0.2:6789)'. Gluetun healthy, nzbget/prowlarr NetworkMode matched Gluetun's Id, but nzbget had exited cleanly (exit 0) at 2026-10-16 23:30:58Z and was not restarted. Action: restarted nzbget via Dockhand API. Result: nzbget running, connection-refused error gone after CheckHealth; Sonarr still lists 'all download clients unavailable due to failures' (backoff), which should clear on its next retry. Cause: Aaron stopped NZBGet on purpose to test the Fix with Claude tap path (see 'Fix-run tap path tested on a real sonarr_health alert'); the run couldn't know that.

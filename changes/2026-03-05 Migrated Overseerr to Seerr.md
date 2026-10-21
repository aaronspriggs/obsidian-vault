---
date: 2026-03-05
type: upgrade
system:
- '[[Servarr Stack (Docker Compose)]]'
notion_id: 31a7ae76-22ba-8161-a8d1-c842e8301806
---

# Migrated Overseerr to Seerr

Migrated from [lscr.io/linuxserver/overseerr:latest](http://lscr.io/linuxserver/overseerr:latest) to [ghcr.io/seerr-team/seerr:latest](http://ghcr.io/seerr-team/seerr:latest). Overseerr is now deprecated upstream. Migration steps: backed up overseerr config to overseerr-backup-20260305, fixed config ownership to UID 1000 (node user), updated compose in Dockhand — image changed, container renamed to seerr, added init: true, removed PUID/PGID, volume path changed from /config to /app/config, added healthcheck. Seerr auto-migrated Overseerr data on first start. Radarr and Sonarr API keys needed to be re-pasted after migration. All services confirmed working, library showing correctly.

---
type: project
status: done
priority: high
system:
- '[[Dockhand]]'
- '[[Dockge]]'
completed: 2026-03-05
notion_id: 3127ae76-22ba-81d4-80a5-f8e85da5312d
---

Dockge not resolving DATA_PATH env var for volume mounts and not reliably writing UI edits to compose.yaml on disk. Portainer has better env var support and stack management. Install Portainer, recreate servarr stack with hardcoded plex_content path, verify /data mounts on all containers, resume downloads.

## Why

Dockge is not resolving `${DATA_PATH}` in volume mounts, causing Radarr/Sonarr/NZBGet to be missing their `/data` mount entirely. Also discovered Dockge UI edits don't reliably write back to compose.yaml on disk.

## Steps

1. Stop servarr stack: `cd "/mnt/Big Boi/BIGBOI/servarr" && sudo docker compose down`
2. Install Portainer (standalone container)
3. Import servarr stack into Portainer using updated compose.yaml (DATA_PATH hardcoded)
4. Verify all containers have both /config and /data mounts via `docker inspect`
5. Resume downloads in NZBGet
6. Verify first completed download imports successfully into Radarr

## Updated compose.yaml

Ready to use — all `${DATA_PATH}:/data` replaced with `/mnt/Big Boi/BIGBOI/plex_content:/data` in nzbget, sonarr, and radarr. VPN vars still use .env substitution.

## Current State (2026-02-24)

- Downloads paused in NZBGet
- Stack running but /data missing from containers
- plex_content ownership correctly set to 3000:0

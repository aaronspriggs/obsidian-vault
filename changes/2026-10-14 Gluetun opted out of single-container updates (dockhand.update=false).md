---
date: 2026-10-14
type: config
system:
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Trial HA Install (Dockhand update entities) for container image updates]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/fc7e579
notion_id: 3f97ae76-22ba-810c-acb6-e8c48df2e5ad
---

# Gluetun opted out of single-container updates (dockhand.update=false)

Approved by Aaron. Label dockhand.update=false on gluetun so HA/Dockhand Install isn't offered for it; Gluetun updates go through a stack deploy. Applied via PUT compose + servarr deploy {forceRecreate} at 16:14 UTC. HA update.big_boi_containers_gluetun now has supported_features 16 (no Install).

**Why:** this prepares for trying HA's Install on Dockhand update entities (see the linked task). Install recreates one container at a time. A Gluetun recreated alone gets a new ID, so NZBGet and Prowlarr (`network_mode: service:gluetun`) lose their network, and `gluetun-watchdog`'s `docker restart` can't reattach them.
**Applied:** repo commit fc7e579, then `PUT /api/stacks/servarr/compose`, then `POST /api/stacks/servarr/deploy {forceRecreate}`. The job finished in ~33 s.
**Checks:** Gluetun is healthy with the new ID a808b3e0e6af. NZBGet and Prowlarr `NetworkMode` = `container:a808b3e0e6af`. All 7 containers are running. Sonarr/Radarr/Prowlarr return 302, NZBGet 401, Seerr 307. HA shows `update.big_boi_containers_gluetun` with `supported_features` 16 (release notes only); the other containers still have 21 (Install).

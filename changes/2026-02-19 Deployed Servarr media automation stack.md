---
date: 2026-02-19
type: install
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 30d7ae76-22ba-815b-a01e-cbc71008ebc1
---

# Deployed Servarr media automation stack

Deployed 6-container Docker Compose stack on TrueNAS: Gluetun (ProtonVPN), NZBGet (Newshosting), Prowlarr (NZBGeek), Sonarr, Radarr, Overseerr. Created storage dirs, configured all services, verified end-to-end pipeline. Changed ZFS aclmode to passthrough on Big Boi/BIGBOI dataset.

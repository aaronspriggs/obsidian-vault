---
date: 2026-03-04
type: config
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[Dockhand]]'
notion_id: 31a7ae76-22ba-81ce-b1c7-fbd838ea9d15
---

# Full servarr stack reconfiguration after Dockhand migration

All 6 servarr services reconfigured from scratch after Dockhand migration reset configs. NZBGet: Newshosting server configured ([news.newshosting.com:563](http://news.newshosting.com:563/), SSL, 30 connections), paths set (MainDir /data/downloads/usenet, DestDir /data/downloads/usenet/completed, InterDir /data/downloads/usenet/intermediate), categories set to 'movies' and 'tv' (lowercase), default credentials changed. Prowlarr: auth configured, NZBGeek indexer added (API key), Sonarr and Radarr connected via Full Sync at internal Docker IPs. Sonarr: auth configured, NZBGet download client added (172.39.0.2:6789, category tv), root folder /data/TV Shows. Radarr: auth configured, NZBGet download client added (172.39.0.2:6789, category movies), root folder /data/Movies. Overseerr: signed in with Plex account, connected to plex-vm (192.168.1.116:32400), Sonarr and Radarr connected. Created missing download directories: /data/downloads/usenet/completed/movies, /data/downloads/usenet/completed/tv, /data/downloads/usenet/intermediate. End-to-end pipeline tested and confirmed working — movie downloaded via Usenet through VPN successfully. Issue encountered: NZBGet orphaned from Gluetun network after Gluetun restart — fixed with docker restart nzbget. WireGuard private key rotated in ProtonVPN.

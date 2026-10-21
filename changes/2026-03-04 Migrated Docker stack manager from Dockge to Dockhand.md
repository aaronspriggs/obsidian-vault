---
date: 2026-03-04
type: config
system:
- '[[Dockhand]]'
- '[[Dockge]]'
notion_id: 31a7ae76-22ba-81d4-b1f4-d22a476f821e
---

# Migrated Docker stack manager from Dockge to Dockhand

Removed Dockge container. Installed Dockhand v1.1.4 via TrueNAS community app catalog on port 3001. Added apps user (UID 568) to docker group (GID 999) to allow catalog app access to Docker socket. Configured Big Boi environment via Unix socket /var/run/docker.sock. Recreated servarr stack in Dockhand with DATA_PATH hardcoded to /mnt/Big Boi/BIGBOI/plex_content:/data (replacing ${DATA_PATH} env var substitution which was unreliable). Generated new ProtonVPN WireGuard config and rotated private key. All 6 containers running: gluetun, nzbget, prowlarr, sonarr, radarr, overseerr.

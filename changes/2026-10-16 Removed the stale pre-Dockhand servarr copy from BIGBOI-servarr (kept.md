---
date: 2026-10-16
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Dockhand]]'
project:
- '[[Plan backup strategy for TrueNAS and VMs]]'
notion_id: 3fb7ae76-22ba-811e-aace-ec9aebfb04eb
---

# Removed the stale pre-Dockhand servarr copy from BIGBOI/servarr (kept overseerr/)

Checked live container mounts via dockhand-api: only seerr uses BIGBOI/servarr (overseerr/ -> /app/config); the other servarr apps mount the Dockhand stack dir. BIGBOI/servarr/compose.yaml and .env (2026-03-05 / 2026-02-20) differed from the live stack copies (2026-10-14 / 2026-09-29), and the stale .env files held old WireGuard config on the SMB-shared dataset. Aaron approved (Tier 3). Claude took manual snapshot Big Boi/BIGBOI@pre-servarr-cleanup-2026-10-16 (no expiry); Aaron ran rm -rf of compose.yaml, .env, servarr/, gluetun/, nzbget/, prowlarr/, radarr/, sonarr/, overseerr-backup-20260304/. Verified: only overseerr/ remains; all containers running, seerr/gluetun/dockhand/kuma healthy. Deleted data also survives 30 days in the daily snapshots and as B2 prior versions. Left as is: the Dockhand app's bind mount of BIGBOI/servarr at /stacks (unused leftover; Dockhand stacks are internal, no external stack paths). Roll back: copy back from /mnt/Big Boi/BIGBOI/.zfs/snapshot/pre-servarr-cleanup-2026-10-16/servarr/.

---
date: 2026-09-24
type: upgrade
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3e57ae76-22ba-81a2-8dcd-f17b602e8736
---

# Upgraded Plex VM: Ubuntu 24.04.5 + kernel 6.8.0-142, Plex 1.43.0 → 1.43.4; set up scoped Claude maintenance access

**Access:** created the `claude` account on the Plex VM. Key-only login from the ClaudeCode VM; root is limited to `/usr/local/sbin/claude-maint`. Aaron generated the key and ran the setup with his plexadmin sudo. See the "Updating the Plex VM (OS + Plex)" runbook.
**Root causes found:**
- The Plex apt repo is stale (newest build 1.42.2, older than the installed 1.43.0), so nightly unattended-upgrades never had a Plex upgrade to install. Fixed by making `claude-maint upgrade-plex` install the latest public .deb from [plex.tv](http://plex.tv/)'s official download API, with URL and SHA-1 checks.
- unattended-upgrades only installs Ubuntu *security* updates (Ubuntu default), so about 75 regular `noble-updates` had piled up.
- The VM hadn't rebooted in 11 weeks. It was running kernel 6.8.0-134 while 136–142 and a libc update were waiting on a reboot.
**Performed:** apt full-upgrade (71 upgraded, 19 new; 4 held back by Ubuntu phased rollout, which is normal), Plex 1.43.0.10492 → **1.43.4.10903**, reboot (Ubuntu 24.04.3 → **24.04.5**, kernel 6.8.0-134 → **6.8.0-142**), autoremove. Rollback point: the daily 00:00 recursive `vmstore` snapshot, which covers the Plex zvol. No active transcodes at start.
**Validated after reboot:** plexmediaserver active and enabled; `/identity` reports 1.43.4 on the VM and over the LAN; NFS `/mnt/media` (ro) and `/mnt/dvr` (rw) automount OK, library folders visible; `/dev/dri` card0/card1/renderD128 present and `plex` in video+render; no failed units; no Plex errors in the journal; root disk 41% used. Hardware transcoding wasn't exercised (no active stream to test with).
**Found, not fixed:** the `/transcode` tmpfs from the Plex page's documented setup no longer exists (not in fstab, not mounted), so transcodes write to the 15 GB root disk. Recorded as a Known Gap on the Plex page. Also corrected stale docs: the NFS mounts use systemd automount now, not a standard boot mount.

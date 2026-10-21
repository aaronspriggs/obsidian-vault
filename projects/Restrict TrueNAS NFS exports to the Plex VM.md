---
type: task
status: done
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
completed: 2026-09-28
notion_id: 3e77ae76-22ba-8138-b5bc-cb7522df65e3
---

Not needed: the exports were already restricted. Verified live 2026-09-28 via the TrueNAS API: plex_content (ro) and plex_recordings (rw) both have hosts = [192.168.1.116], networks = []. The 2026-09-26 finding read the empty `networks` field and missed `hosts`. The TrueNAS audit log (7-day retention) shows no sharing.nfs changes since, so nothing was changed.

In TrueNAS Shares → NFS, set Authorized Hosts/Networks on both exports to **192.168.1.116** (Plex VM). Then check that the Plex VM still automounts `/mnt/media` and `/mnt/dvr` (`ls` both, or run `homelab-update test` on the Plex VM, which checks both mounts) and that Plex playback works. Low risk, but test right after the change.

---
date: 2026-10-23
type: fix
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Plan backup strategy for TrueNAS and VMs]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/8654a3b
---

# B2 vmstore sync stages consistent servarr DBs and skips logs

The one-week B2 bucket check found `B2 offsite: vmstore` re-uploading ~705 files / ~205 MiB every night (details in [[Plan backup strategy for TrueNAS and VMs]]). Sonarr, Radarr, Prowlarr, NZBGet and Gluetun keep their live config in Dockhand's stack dir (compose `./<app>:/config`), so the 23:30 TrueNAS cron is their only backup. Its rsync copied rotating debug logs (~290 MiB, renumbered on every rollover) and Prowlarr's 670 indexer definitions (rewritten daily), and copied the apps' WAL-mode SQLite DBs while they were running, so the raw DB copies could be torn. The Plex export was also re-staged with a fresh mtime every night.

Aaron approved the fix 2026-10-23. Claude changed the repo ([8654a3b](https://github.com/aaronspriggs/spriggs-homelab/commit/8654a3b)) and Aaron applied it in the TrueNAS UI (`claude-maint` has no cron or Cloud Sync rights):

- Cron job 1 now runs `rsync -a --delete --delete-excluded --exclude=logs/ --exclude=Definitions/ ...` (the raw `*.db` files stay in the copy so a future stack's DB is never silently dropped).
- The vmstore pre-script `sqlite_copy`s `sonarr.db`, `radarr.db` and `prowlarr.db` into `offsite-staging` and stages the Plex export with `cp -p`.
- [[Offsite backup to B2 - what's covered and how to restore]] now restores the staged DBs over the raw ones.

**Verified:** `make check` shows the task's pre-script matches the repo, and the cron command matches `truenas/README.md` (its UI description still has the old wording, cosmetic). Manual run 16:16 UTC: SUCCESS, 24 files / 118.8 MiB (the night before: 750 / 256.9 MiB); the stacks copy no longer has `logs/` or `Definitions/`; the three DBs are staged (sonarr 17.1, radarr 2.6, prowlarr 2.2 MiB) and `plex-db.tar.gz` kept its 10-19 mtime. Expected steady nightly upload is roughly 60–70 MiB (Dockhand's DB alone is 36 MiB gzipped) and the 30-day bucket steady state about 4–5 GB instead of ~10 GB.

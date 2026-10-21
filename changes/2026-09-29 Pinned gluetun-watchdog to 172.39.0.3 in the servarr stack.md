---
date: 2026-09-29
type: fix
system:
- '[[Servarr Stack (Docker Compose)]]'
project:
- '[[Add health checks and autoheal to servarr stack]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/c3c791d
notion_id: 3ea7ae76-22ba-813b-b45e-c7f7c40bd8e9
---

# Pinned gluetun-watchdog to 172.39.0.3 in the servarr stack

Watchdog pinned so it can't take Gluetun's 172.39.0.2 during a recreate. Repo first, then Dockhand Save and redeploy (full-stack force-recreate). Verified: gluetun .2, watchdog .3, NZBGet/Prowlarr on the current Gluetun ID, all 5 UIs up within about a minute.

**Before:** the live Dockhand compose matched the repo (same 3592 bytes, mtime 2026-07-11), so the repo copy was a safe base.
**Apply:** Aaron edited the watchdog's `networks:` block in Dockhand. The first attempt failed YAML parsing (go-yaml "mapping values are not allowed" at L47, most likely the old `- servarrnetwork` list dash left in place). Dockhand saves the file before validating, so the broken text sat on disk until the fix. The containers kept running. The corrected file is byte-identical in size to the repo (3698).
**Found along the way:** Dockhand's Save and redeploy runs `docker compose up -d --force-recreate`, which recreates all 7 containers ([Finsys/dockhand#419](https://github.com/Finsys/dockhand/issues/419), open). Added to the servarr runbook, together with the alternative of recreating a single service from the CLI.
**Verify (Aaron, over SSH):** `servarrnetwork` shows gluetun 172.39.0.2, gluetun-watchdog .3, sonarr .5, radarr .6, seerr .7; nzbget and prowlarr `container:d54b0847…` = current Gluetun ID. Sonarr, Radarr, Prowlarr, NZBGet and Seerr all answered from the ClaudeCode VM by 22:39 UTC.
**Backups relied on:** the nightly Dockhand stacks rsync to `vmstore` (the 2026-09-29 copy includes the app config dirs, e.g. the 17.8 MB sonarr.db).

---
date: 2026-02-24
type: fix
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3127ae76-22ba-81f6-860d-dedad0f9eaf0
---

# Fixed Radarr/Sonarr import failure — plex_content ownership

plex_content directory and subdirectories were owned by root:root. Containers run as PUID=3000 (aspriggs)/PGID=0, so Radarr couldn't see /data/Movies inside the container. Fixed with: sudo chown -R 3000:0 "/mnt/Big Boi/BIGBOI/plex_content/". All 8 affected movies (Zombieland, The Martian, Ex Machina, Ocean's Eleven, D&D, Weird Al, Ford v Ferrari, Inception) had to be re-downloaded as NZBGet had already purged completed files. Root cause: initial stack deployment left ownership as root. Marty Supreme succeeded first time by luck.

## Problem

Movies requested through Overseerr downloaded successfully via NZBGet but never appeared in Plex. Radarr showed all movies as Queued (purple) indefinitely.

## Root Cause

`/mnt/Big Boi/BIGBOI/plex_content/` and all subdirectories were owned by `root:root`. Servarr containers run as PUID=3000 (aspriggs) / PGID=0. With `rwxrwx---` permissions, UID 3000 had no access, so Radarr couldn't resolve `/data/Movies` inside the container.
Radarr logs: `RootFolderNotFoundException: Root folder '/data/Movies' was not found.`
NZBGet cleaned up completed downloads before Radarr could import them.

## Fix

```bash
sudo chown -R 3000:0 "/mnt/Big Boi/BIGBOI/plex_content/"
```
Verified with write test — new files created as `aspriggs root`.

## Recovery

8 movies re-triggered via Radarr Movie Editor → Search All. Currently re-downloading.

## Gotcha Added

Added to servarr gotchas: plex_content must be owned by 3000:0, not root:root. Verify after any TrueNAS ACL changes or dataset operations.

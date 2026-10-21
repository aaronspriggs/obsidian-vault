---
date: 2026-10-15
type: config
system:
- '[[Dockhand]]'
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Prune old Docker images on TrueNAS]]'
notion_id: 3fa7ae76-22ba-81c8-b7e4-d289c52aacd5
---

# Pruned 21 unused Docker images on Big Boi and enabled weekly Dockhand image prune

21 images / 7.4 GB removed via Dockhand API (Tier 3, Aaron yes); image prune on, weekly, dangling only.

## What changed

- **Deleted 21 Docker images that no container used.** `fnsys/dockhand:v1.0.20`, `lscr.io/linuxserver/overseerr:latest`, and 19 untagged old versions from Jan–Sep 2026, 7.4 GB in all. Big Boi now has 11 images, 4.2 GB, all in use.
- **Turned on Dockhand image prune for Big Boi:** weekly, cron `0 3 * * 0` in the environment's UTC timezone, `dangling` mode.

## Why

Every image update leaves the previous version on disk untagged, and nothing was pruning them. Aaron approved the delete (Tier 3) and the schedule on 2026-10-15.

## How

1. `dockhand-api "/api/images?env=1"`, then pick the images with `containers == 0`. Snapshots of the image and container lists before the change are in the session scratchpad.
2. `dockhand-api --write DELETE "/api/images/<id>?env=1"` for each one. All 21 returned `success: true`.
3. `dockhand-api --write POST /api/environments/1/image-prune '{"enabled":true,"cronExpression":"0 3 * * 0","pruneMode":"dangling"}'`. PUT failed with "settings not found" because no row existed yet.

## Verify / roll back

- `dockhand-api /api/environments/1/image-prune` shows `enabled: true`. `imagePruneEnabled` is true on environment 1. The containers list was unchanged afterwards (10 running, the permissions helper exited as usual).
- To roll back the schedule, POST the same body with `enabled: false`. Deleted images can be re-pulled by tag if ever needed.

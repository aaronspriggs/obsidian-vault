---
type: task
status: done
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Dockhand]]'
completed: 2026-10-15
notion_id: 3e77ae76-22ba-815d-8ffb-f88acf96954b
---

21 unused images (7.4 GB) deleted 2026-10-15; weekly dangling-image prune enabled in Dockhand.

## Outcome (Done 2026-10-15)

Deleted 21 unused images on Big Boi through the Dockhand API (`DELETE /api/images/<id>?env=1`), with Aaron's yes on 2026-10-15. Big Boi went from 32 images / 7.4 GB unused to 11 images, 4.2 GB in total, all in use. The images removed were `fnsys/dockhand:v1.0.20`, `lscr.io/linuxserver/overseerr:latest` and 19 untagged old versions. All 11 containers were in the same state afterwards (10 running, plus `ix-dockhand-permissions-1` exited as usual).
**Why they piled up:** each image update pulls the new version under the same tag, and the old one stays on disk untagged (dangling). Nothing pruned them, because Dockhand's image prune was off for Big Boi.
**Fix:** Dockhand image prune is now on for Big Boi. It runs weekly, cron `0 3 * * 0` in the environment's UTC timezone (Saturday 21:00 Mountain daylight time), in `dangling` mode, so it only removes untagged images. It's set with `POST /api/environments/1/image-prune`. Use POST because PUT fails until the settings row exists. Read it back with `GET` on the same path.

## Decisions

- **2026-10-15:** use `dangling` mode, not prune-all-unused. Tagged images that are unused but deliberately kept (e.g. a pinned rollback) survive. To roll back an app, re-pull its version tag; the dangling image isn't the rollback path.

## Links

Changes: "Pruned 21 unused Docker images on Big Boi and enabled weekly Dockhand image prune" (2026-10-15).

## Changes

![[Changes.base#For this project]]

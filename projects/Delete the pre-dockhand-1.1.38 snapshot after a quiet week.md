---
type: task
status: backlog
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Dockhand]]'
parent: '[[Decide backup for the Dockhand TrueNAS app upgrade, then upgrade it]]'
next_step: 'From 2026-10-22: if Dockhand v1.0.53 has been fine, Claude deletes the three snapshots (Tier 2: say it, then do it).'
notion_id: 3fa7ae76-22ba-8179-b361-d0f2a6807d42
---

Manual recursive snapshot Big Boi/ix-apps/app_mounts@pre-dockhand-1.1.38 (taken 2026-10-15 before the Dockhand upgrade); no periodic task expires it. Delete with truenas-api --write zfs.snapshot.delete, once each for app_mounts, app_mounts/dockhand and app_mounts/dockhand/data.
